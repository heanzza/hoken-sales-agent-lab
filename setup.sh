#!/usr/bin/env bash
# 法人営業AIエージェント・ラボ — デモ環境セットアップ
# 利用データ(テーブル/ビュー/用語集/Metric View)を作成し、商品PDFをVolumeに配置します。
#
# 前提: Databricks CLI (v0.292+) が認証済みであること。
# 使い方:
#   PROFILE=<your-profile> ./setup.sh
#   （任意で CATALOG / SCHEMA / VOLUME を上書き可能）
set -euo pipefail

PROFILE="${PROFILE:?PROFILE を指定してください (例: PROFILE=jp-fsi ./setup.sh)}"
CATALOG="${CATALOG:-jp_fsi_catalog}"
SCHEMA="${SCHEMA:-houjin_eigyo}"
VOLUME="${VOLUME:-product_docs}"
HERE="$(cd "$(dirname "$0")" && pwd)"

echo "▶ Profile=$PROFILE  Target=$CATALOG.$SCHEMA  Volume=$VOLUME"

# スキーマ作成(なければ)
databricks experimental aitools tools query \
  "CREATE SCHEMA IF NOT EXISTS \`$CATALOG\`.\`$SCHEMA\`" --profile "$PROFILE" >/dev/null
echo "✔ schema ready"

# --- 前提テーブル(契約・マスタ)チェック ---
# houjin_keiyaku / channel_master / shohin_master / shibu_master が必要です。
# 既存の houjin_eigyo デモ資産を利用します。無い場合は別途ご用意ください。
MISSING=$(databricks experimental aitools tools query \
  "SELECT concat_ws(',', collect_list(t)) AS missing FROM (
     SELECT 'houjin_keiyaku' t UNION ALL SELECT 'channel_master' UNION ALL
     SELECT 'shohin_master' UNION ALL SELECT 'shibu_master'
   ) x WHERE t NOT IN (SELECT table_name FROM \`$CATALOG\`.information_schema.tables WHERE table_schema='$SCHEMA')" \
  --profile "$PROFILE" 2>/dev/null | python3 -c "import json,sys;d=json.load(sys.stdin);print(d[0]['missing'] if d and d[0].get('missing') else '')" || echo "")
if [ -n "$MISSING" ]; then
  echo "⚠ 前提テーブルが不足しています: $MISSING"
  echo "  （houjin_keiyaku 等の法人契約ファクト/マスタが必要です。README の『前提データ』を参照）"
fi

# --- SQL 実行 ---
python3 - "$PROFILE" "$CATALOG" "$SCHEMA" "$HERE" <<'PY'
import subprocess, sys, glob, os
profile, catalog, schema, here = sys.argv[1:5]
files = sorted(glob.glob(os.path.join(here, "sql", "*.sql")))
for f in files:
    sql = open(f).read().replace("jp_fsi_catalog.houjin_eigyo", f"{catalog}.{schema}")
    stmts = [s.strip() for s in sql.split("-- SPLIT --") if s.strip()]
    okc = 0
    for s in stmts:
        r = subprocess.run(["databricks","experimental","aitools","tools","query",s,"--profile",profile],
                           capture_output=True, text=True)
        out = (r.stdout + r.stderr).strip()
        if r.returncode != 0 or "Error" in out:
            print(f"  ✖ {os.path.basename(f)} :: {out[:200]}")
        else:
            okc += 1
    print(f"✔ {os.path.basename(f)}  ({okc}/{len(stmts)} statements)")
PY

# --- Volume 作成 & 商品PDF アップロード ---
databricks volumes create "$CATALOG" "$SCHEMA" "$VOLUME" MANAGED --profile "$PROFILE" >/dev/null 2>&1 \
  && echo "✔ volume created: $CATALOG.$SCHEMA.$VOLUME" \
  || echo "• volume exists: $CATALOG.$SCHEMA.$VOLUME"
for f in "$HERE"/product_docs/pdf/*.pdf; do
  [ -e "$f" ] || continue
  databricks fs cp "$f" "dbfs:/Volumes/$CATALOG/$SCHEMA/$VOLUME/$(basename "$f")" --overwrite --profile "$PROFILE" >/dev/null
done
echo "✔ product PDFs uploaded"

cat <<EOF

──────────────────────────────────────────
✅ 利用データのセットアップ完了

次のステップ:
  1. Genie Space を作成     : PROFILE=$PROFILE WAREHOUSE=<warehouse_id> ./genie/create_genie_spaces.sh
  2. Pages を投入(UI/Beta)   : pages/houjin_eigyo_pages.md を Discover→Domain→Pages で取り込み
  3. Knowledge Assistant(UI) : Volume /Volumes/$CATALOG/$SCHEMA/$VOLUME の上に作成
  4. Multi-Agent Supervisor  : Genie + KA を束ねて作成
  （3・4 の詳細手順は README.md / docs/handson.html を参照）
──────────────────────────────────────────
EOF
