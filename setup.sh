#!/usr/bin/env bash
# 法人営業AIエージェント・ラボ — セットアップ補助 (CLI)
#
# このスクリプトは「ワークスペースへの取り込み」だけを行います。
#   1) セットアップ用ノートブック(notebooks/)をワークスペースにインポート
#   2) 商品資料PDFを Volume にアップロード
# データ本体の作成は、インポートした 01_setup_sample_data ノートブックを
# 「すべて実行」して行います(下記の案内を参照)。
#
# 前提: Databricks CLI (v0.292+) が認証済みであること。
# 使い方:
#   PROFILE=<your-profile> ./setup.sh
#   （任意で CATALOG / SCHEMA / VOLUME / WORKSPACE_DIR を上書き可能）
set -euo pipefail

PROFILE="${PROFILE:?PROFILE を指定してください (例: PROFILE=jp-fsi ./setup.sh)}"
CATALOG="${CATALOG:-jp_fsi_catalog}"
SCHEMA="${SCHEMA:-houjin_eigyo}"
VOLUME="${VOLUME:-product_docs}"
HERE="$(cd "$(dirname "$0")" && pwd)"
ME="$(databricks current-user me --profile "$PROFILE" -o json | python3 -c 'import json,sys;print(json.load(sys.stdin)["userName"])')"
WORKSPACE_DIR="${WORKSPACE_DIR:-/Workspace/Users/$ME/hoken_sales_agent_lab}"

echo "▶ Profile=$PROFILE  Target=$CATALOG.$SCHEMA  Volume=$VOLUME"
echo "▶ Notebooks → $WORKSPACE_DIR"

# 1) ノートブックをインポート
databricks workspace mkdirs "$WORKSPACE_DIR" --profile "$PROFILE" >/dev/null 2>&1 || true
databricks workspace import-dir "$HERE/notebooks" "$WORKSPACE_DIR" --overwrite --profile "$PROFILE"
echo "✔ notebooks imported"

# 2) スキーマ・ボリュームを用意し、商品PDFをアップロード
#    (00_config でも冪等に作成されますが、ここで作っておくと先にPDFを置けます)
databricks schemas create "$SCHEMA" "$CATALOG" --profile "$PROFILE" >/dev/null 2>&1 \
  && echo "✔ schema created: $CATALOG.$SCHEMA" || echo "• schema exists: $CATALOG.$SCHEMA"
databricks volumes create "$CATALOG" "$SCHEMA" "$VOLUME" MANAGED --profile "$PROFILE" >/dev/null 2>&1 \
  && echo "✔ volume created: $CATALOG.$SCHEMA.$VOLUME" || echo "• volume exists: $CATALOG.$SCHEMA.$VOLUME"
for f in "$HERE"/product_docs/pdf/*.pdf; do
  [ -e "$f" ] || continue
  databricks fs cp "$f" "dbfs:/Volumes/$CATALOG/$SCHEMA/$VOLUME/$(basename "$f")" --overwrite --profile "$PROFILE" >/dev/null
done
echo "✔ product PDFs uploaded → /Volumes/$CATALOG/$SCHEMA/$VOLUME"

cat <<EOF

──────────────────────────────────────────
✅ 取り込み完了。次にワークスペースで:

  1. $WORKSPACE_DIR/01_setup_sample_data を開く
     → ウィジェットで catalog=$CATALOG / schema=$SCHEMA を確認し【すべて実行】
       (先頭で %run ./00_config が実行され、テーブル/ビュー/用語集/Metric View が作成されます)

  2. Genie Space を作成:
     PROFILE=$PROFILE WAREHOUSE=<warehouse_id> ./genie/create_genie_spaces.sh

  3. Pages 投入(UI/Beta): pages/houjin_eigyo_pages.md を Discover→Domain→Pages で取り込み
  4. Knowledge Assistant / Multi-Agent Supervisor(UI): README.md / docs/handson.html 参照
──────────────────────────────────────────
EOF
