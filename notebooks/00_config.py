# Databricks notebook source
# MAGIC %md
# MAGIC # 00_config — 法人営業AIエージェント・ラボ
# MAGIC 
# MAGIC カタログ / スキーマ / ボリュームを設定し、無ければ作成します。`01_setup_sample_data` から `%run ./00_config` で読み込まれます。
# MAGIC 
# MAGIC ウィジェットで対象を切り替えできます（既定: `jp_fsi_catalog.houjin_eigyo`）。

# COMMAND ----------

dbutils.widgets.text("catalog", "jp_fsi_catalog", "カタログ")
dbutils.widgets.text("schema",  "houjin_eigyo",  "スキーマ")
dbutils.widgets.text("volume",  "product_docs",  "商品資料ボリューム")

catalog = dbutils.widgets.get("catalog")
schema  = dbutils.widgets.get("schema")
volume  = dbutils.widgets.get("volume")

# COMMAND ----------

# カタログは既存前提。スキーマ・ボリュームは無ければ作成
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {catalog}.{schema}.{volume}")
spark.sql(f"USE CATALOG {catalog}")
spark.sql(f"USE SCHEMA {schema}")

print(f"catalog = {catalog}")
print(f"schema  = {schema}")
print(f"volume  = /Volumes/{catalog}/{schema}/{volume}")
