#!/usr/bin/env bash
# Genie Space を2つ作成:
#   1) 法人営業アシスタント (キュレーション済み / 本命)
#   2) 【Before】用語集・文脈なし (対比用)
#
# 使い方:
#   PROFILE=<profile> WAREHOUSE=<warehouse_id> ./genie/create_genie_spaces.sh
#   （任意で CATALOG / SCHEMA / PARENT_PATH を上書き可能）
set -euo pipefail

PROFILE="${PROFILE:?PROFILE を指定してください}"
WAREHOUSE="${WAREHOUSE:?WAREHOUSE(SQL Warehouse ID) を指定してください}"
CATALOG="${CATALOG:-jp_fsi_catalog}"
SCHEMA="${SCHEMA:-houjin_eigyo}"
HERE="$(cd "$(dirname "$0")" && pwd)"

# parent_path (存在する必要あり)。既定はカレントユーザーの genie_spaces フォルダ。
ME="$(databricks current-user me --profile "$PROFILE" -o json | python3 -c 'import json,sys;print(json.load(sys.stdin)["userName"])')"
PARENT_PATH="${PARENT_PATH:-/Workspace/Users/$ME/genie_spaces}"
databricks workspace mkdirs "$PARENT_PATH" --profile "$PROFILE" >/dev/null 2>&1 || true

create_space () {
  local file="$1" title="$2" desc="$3"
  local json
  json="$(python3 -c "import sys;print(sys.stdin.read().replace('jp_fsi_catalog.houjin_eigyo','${CATALOG}.${SCHEMA}'))" < "$file")"
  databricks genie create-space --profile "$PROFILE" --json "{
    \"warehouse_id\": \"$WAREHOUSE\",
    \"title\": \"$title\",
    \"description\": \"$desc\",
    \"parent_path\": \"$PARENT_PATH\",
    \"serialized_space\": $(printf '%s' "$json" | jq -c '.' | jq -Rs '.')
  }" | python3 -c 'import json,sys;d=json.load(sys.stdin);print("  space_id:",d.get("space_id"),"|",d.get("title"))'
}

echo "▶ Genie Space 作成 (parent=$PARENT_PATH)"
create_space "$HERE/genie_agent.json" \
  "法人営業アシスタント (ハンズオン)" \
  "法人営業の担当企業分析・課題抽出・提案検討を支援。社内用語(shanai_ryakugo)を参照し、企業360度ビュー・KPIメトリックビューでキュレーション済み。"
create_space "$HERE/genie_before.json" \
  "【Before】法人営業データ (用語集・文脈なし)" \
  "対比用: 生データのみで用語集/文脈/instructionを与えていない素の状態。"
echo "✔ done — 出力された space_id を docs/handson.html / スライドの接続情報に反映してください。"
