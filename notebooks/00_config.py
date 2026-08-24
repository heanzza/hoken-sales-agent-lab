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
CATALOG = "jp_fsi_catalog"
SCHEMA  = "houjin_eigyo"
VOLUME  = "product_docs"   # 商品資料PDFの置き場

# ==========================================================
# 以下は自動導出（変更不要）
# ==========================================================
def tbl(name: str) -> str:
    """テーブル名を完全修飾名 catalog.schema.name に変換するヘルパ"""
    return f"{CATALOG}.{SCHEMA}.{name}"

# 本ラボが作成する資産
TANTOU_KIGYO      = tbl("tantou_kigyo")       # 担当企業プロファイル
SHODAN_KATSUDO    = tbl("shodan_katsudo")     # 商談活動履歴
V_KEIYAKU_ENRICHED= tbl("v_keiyaku_enriched") # 契約×マスタ 事前結合ビュー
V_EIGYO_360       = tbl("v_eigyo_360")        # 企業360°ビュー
MV_EIGYO_KPI      = tbl("mv_eigyo_kpi")       # KPIメトリックビュー

# 前提（既存の法人契約デモ資産）
HOUJIN_KEIYAKU    = tbl("houjin_keiyaku")     # 法人契約ファクト（前提）
CHANNEL_MASTER    = tbl("channel_master")     # 販売チャネルマスタ（前提）
SHOHIN_MASTER     = tbl("shohin_master")      # 商品マスタ（前提）
SHIBU_MASTER      = tbl("shibu_master")       # 支社マスタ（前提）

VOLUME_PATH       = f"/Volumes/{CATALOG}/{SCHEMA}/{VOLUME}"

print(f"⚙️  共通設定をロードしました:  CATALOG={CATALOG}  SCHEMA={SCHEMA}")
print(f"    例) TANTOU_KIGYO = {TANTOU_KIGYO}")
