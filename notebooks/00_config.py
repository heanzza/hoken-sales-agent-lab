# Databricks notebook source
# DBTITLE 1,共通設定（config）
# MAGIC %md
# MAGIC # 00_config — 法人営業AIエージェント・ラボ 共通設定
# MAGIC
# MAGIC このノートブックは **カタログ・スキーマ等の共通変数** を一元管理します。
# MAGIC 各ノートブックは冒頭で `%run ./00_config` を実行してこれらの変数を取り込みます。
# MAGIC
# MAGIC > 🔧 **環境を変えるときはこの `CATALOG` / `SCHEMA` の2行だけ** 変更すれば全体に反映されます。
# MAGIC
# MAGIC ※ 副作用（テーブル作成やUSE文）を持たないため、通常ノートブックからも安全に `%run` できます。

# COMMAND ----------

# DBTITLE 1,共通変数
# ==========================================================
# ★ ここだけ環境に合わせて変更してください
# ==========================================================
CATALOG = "handson"
SCHEMA  = "hoken_sales"

# ==========================================================
# 以下は自動導出（変更不要）
# ==========================================================
def tbl(name: str) -> str:
    """テーブル名を完全修飾名 catalog.schema.name に変換するヘルパ"""
    return f"{CATALOG}.{SCHEMA}.{name}"

# 本ラボが作成するテーブル
CUSTOMERS       = tbl("customers")        # 顧客マスター（担当企業）
SHOUDAN_HISTORY = tbl("shoudan_history")  # 商談履歴

print(f"⚙️  共通設定をロードしました:  CATALOG={CATALOG}  SCHEMA={SCHEMA}")
print(f"    例) CUSTOMERS = {CUSTOMERS}")
