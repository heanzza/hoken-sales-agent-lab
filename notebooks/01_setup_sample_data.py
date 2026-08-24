# Databricks notebook source
# DBTITLE 1,タイトル
# MAGIC %md
# MAGIC # 法人営業AIエージェント デモ用サンプルデータ
# MAGIC ## 01: サンプルデータのセットアップ
# MAGIC
# MAGIC 保険会社の法人営業における担当企業の顧客マスターと商談履歴データを作成します。
# MAGIC
# MAGIC **作成するテーブル：**
# MAGIC - `customers` — 顧客マスター（担当企業 10社）
# MAGIC - `shoudan_history` — 商談履歴（15件）

# COMMAND ----------

# DBTITLE 1,共通設定を読み込み
# MAGIC %run ./00_config

# COMMAND ----------

# DBTITLE 1,カタログ・スキーマ作成
# === カタログ・スキーマが存在しなければ作成 ===（CATALOG / SCHEMA は 00_config で定義）
# カタログ作成には metastore の CREATE CATALOG 権限が必要。権限が無い場合は既存カタログを使用。
try:
    spark.sql(f"CREATE CATALOG IF NOT EXISTS {CATALOG}")
    print(f"✓ カタログ '{CATALOG}' を確認/作成しました")
except Exception as e:
    print(f"ℹ️ カタログ作成はスキップ（既存カタログ '{CATALOG}' を使用）: {str(e)[:120]}")

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")
spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")
print(f"✓ スキーマ '{CATALOG}.{SCHEMA}' を確認/作成しました")

# COMMAND ----------

# DBTITLE 1,顧客マスター作成
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

# === 顧客マスター（担当企業） ===
customer_data = [
    ("C001", "東京製造株式会社", "製造業", "東京都品川区", "代表取締役 山田太郎", "総務部 鈴木一郎", "03-1234-5678", "suzuki@tokyo-seizou.co.jp", 1500, 85.0, "A", "田中営業部長", "2020-04-01"),
    ("C002", "大阪商事株式会社", "卸売業", "大阪府大阪市北区", "代表取締役 佐藤次郎", "経理部 高橋花子", "06-2345-6789", "takahashi@osaka-shoji.co.jp", 800, 42.0, "B", "田中営業部長", "2019-07-15"),
    ("C003", "名古屋テクノロジー株式会社", "情報通信業", "愛知県名古屋市中区", "代表取締役 伊藤三郎", "人事部 渡辺美咲", "052-3456-7890", "watanabe@nagoya-tech.co.jp", 2200, 120.5, "A", "山本主任", "2018-01-10"),
    ("C004", "福岡物流株式会社", "運輸業", "福岡県福岡市博多区", "代表取締役 小林四郎", "管理部 中村健太", "092-4567-8901", "nakamura@fukuoka-logistics.co.jp", 350, 18.5, "C", "山本主任", "2021-11-20"),
    ("C005", "横浜建設株式会社", "建設業", "神奈川県横浜市中区", "代表取締役 加藤五郎", "総務部 松本直樹", "045-5678-9012", "matsumoto@yokohama-kensetsu.co.jp", 600, 35.0, "B", "田中営業部長", "2022-03-01"),
    ("C006", "札幌食品株式会社", "食料品製造業", "北海道札幌市中央区", "代表取締役 吉田六郎", "総務課 斉藤愛", "011-6789-0123", "saito@sapporo-foods.co.jp", 450, 22.0, "B", "山本主任", "2020-09-01"),
    ("C007", "仙台エネルギー株式会社", "電気・ガス業", "宮城県仙台市青葉区", "代表取締役 山口七郎", "財務部 井上大輔", "022-7890-1234", "inoue@sendai-energy.co.jp", 3000, 200.0, "S", "田中営業部長", "2017-06-15"),
    ("C008", "広島自動車部品株式会社", "製造業", "広島県広島市南区", "代表取締役 林八郎", "購買部 木村翔太", "082-8901-2345", "kimura@hiroshima-autoparts.co.jp", 1200, 65.0, "A", "山本主任", "2019-02-28"),
    ("C009", "神戸港運株式会社", "倉庫・運輸業", "兵庫県神戸市中央区", "代表取締役 清水九郎", "業務部 山下理恵", "078-9012-3456", "yamashita@kobe-harbor.co.jp", 700, 38.0, "B", "田中営業部長", "2021-05-10"),
    ("C010", "京都ホテルグループ株式会社", "宿泊業", "京都府京都市下京区", "代表取締役 前田十郎", "経営企画室 小川真由", "075-0123-4567", "ogawa@kyoto-hotel-group.co.jp", 900, 48.0, "A", "山本主任", "2023-01-15"),
]

customer_schema = StructType([
    StructField("顧客ID", StringType(), False),
    StructField("企業名", StringType(), False),
    StructField("業種", StringType(), True),
    StructField("所在地", StringType(), True),
    StructField("代表者名", StringType(), True),
    StructField("担当者名", StringType(), True),
    StructField("電話番号", StringType(), True),
    StructField("メールアドレス", StringType(), True),
    StructField("従業員数", IntegerType(), True),
    StructField("年間売上_億円", DoubleType(), True),
    StructField("顧客ランク", StringType(), True),
    StructField("営業担当", StringType(), True),
    StructField("契約開始日", StringType(), True),
])

df_customers = spark.createDataFrame(customer_data, schema=customer_schema)
print("=== 顧客マスター（担当企業一覧） ===")
display(df_customers)

# COMMAND ----------

# DBTITLE 1,商談履歴作成
# === 商談履歴 ===
shoudan_data = [
    ("S001", "C001", "東京製造株式会社", "企業総合保険の更新提案", "2026-06-10", "訪問", "提案中", "企業総合保険", 1500, "現行契約が9月満期。補償範囲の拡大を提案。工場の新設備導入に伴い、動産総合保険の追加も検討中。", "次回8/20に見積提示予定", "田中営業部長"),
    ("S002", "C001", "東京製造株式会社", "サイバーリスク保険の新規提案", "2026-07-15", "オンライン", "初回面談", "サイバーリスク保険", 500, "DX推進中でセキュリティリスクへの関心が高い。情報システム部の佐々木部長も同席。競合他社からも提案を受けている模様。", "リスク診断レポートを送付済み", "田中営業部長"),
    ("S003", "C002", "大阪商事株式会社", "賠償責任保険の増額", "2026-05-20", "訪問", "見積提示", "賠償責任保険", 300, "海外取引先の増加に伴い、PL保険の補償額引き上げを希望。米国向け輸出のリスクカバーが焦点。", "見積3パターン提示済み。来週回答予定", "田中営業部長"),
    ("S004", "C003", "名古屋テクノロジー株式会社", "役員賠償責任保険(D&O)の提案", "2026-08-01", "訪問", "提案中", "D&O保険", 800, "来年のIPO準備に向けてD&O保険の導入を検討。証券会社からの推薦あり。補償限度額と免責条項の詳細を求められた。", "8/25に取締役会で検討予定", "山本主任"),
    ("S005", "C003", "名古屋テクノロジー株式会社", "従業員福利厚生プランの拡充", "2026-07-01", "オンライン", "成約", "団体生命保険", 2000, "従業員2200名向けの団体生命保険を成約。月払い保険料の企業負担軽減プランを採用。人事部渡辺様が窓口。", "9月1日付で契約開始", "山本主任"),
    ("S006", "C004", "福岡物流株式会社", "運送業者貨物保険の見直し", "2026-06-25", "電話", "ヒアリング", "貨物保険", 200, "現行の貨物保険でカバーされていない高額貨物の取り扱いが増加。冷凍食品輸送の温度管理リスクも相談あり。", "現行証券のコピーを依頼中", "山本主任"),
    ("S007", "C005", "横浜建設株式会社", "建設工事保険の新規案件", "2026-08-05", "訪問", "提案中", "建設工事保険", 1200, "横浜市の大型再開発プロジェクト（工期3年）に対応する建設工事保険。JV構成企業3社の共同付保を検討。", "JVパートナー企業との調整が必要", "田中営業部長"),
    ("S008", "C006", "札幌食品株式会社", "PL保険とリコール保険のセット提案", "2026-07-20", "オンライン", "提案中", "PL保険", 350, "新商品ラインの全国展開に伴い、PL保険の増額とリコール費用保険の追加を提案。食品衛生法改正への対応も含む。", "品質管理部との合同MTG調整中", "山本主任"),
    ("S009", "C007", "仙台エネルギー株式会社", "包括保険プログラムの年次レビュー", "2026-08-10", "訪問", "見積提示", "企業包括保険", 5000, "年間保険料2億円超の主力顧客。火力発電所の定期修繕に合わせた保険設計の見直し。再保険マーケットの動向を踏まえた料率交渉中。", "9月末の満期更改に向けて最終調整", "田中営業部長"),
    ("S010", "C007", "仙台エネルギー株式会社", "再生可能エネルギー事業のリスク評価", "2026-07-28", "訪問", "初回面談", "再エネ保険", 3000, "洋上風力発電プロジェクト（2028年稼働予定）の保険スキーム構築。建設期間中のリスクと稼働後の利益保険を一括提案予定。", "ロンドンマーケットへの照会開始", "田中営業部長"),
    ("S011", "C008", "広島自動車部品株式会社", "海外PL保険の拡大", "2026-06-15", "オンライン", "失注", "海外PL保険", 600, "北米向け自動車部品のPL保険拡大を提案したが、グループ親会社の包括契約に統合される方針となり失注。", "親会社の保険担当と情報交換予定", "山本主任"),
    ("S012", "C009", "神戸港運株式会社", "労災上乗せ保険の提案", "2026-08-15", "訪問", "初回面談", "労災上乗せ保険", 250, "港湾作業員の労災事故が前年比増加。現行の政府労災に加え、上乗せ補償の導入を検討。安全管理コンサル付きプランに関心。", "過去3年の事故データを分析中", "田中営業部長"),
    ("S013", "C010", "京都ホテルグループ株式会社", "施設賠償保険と休業補償の見直し", "2026-07-10", "訪問", "提案中", "施設賠償保険", 400, "インバウンド回復で宿泊者数が過去最高を更新。施設賠償の補償額引き上げと、感染症による休業リスクのカバーを希望。", "3施設の現地調査を8月中に実施予定", "山本主任"),
    ("S014", "C010", "京都ホテルグループ株式会社", "新規ホテル開業に伴う保険設計", "2026-08-20", "訪問", "ヒアリング", "総合保険", 600, "2027年春開業予定の新ホテル（150室）の保険パッケージ設計。建設期間中の工事保険から開業後の営業保険への切り替えスキームを提案予定。", "設計図面と事業計画書の入手待ち", "山本主任"),
    ("S015", "C002", "大阪商事株式会社", "取引信用保険の新規提案", "2026-08-18", "オンライン", "初回面談", "取引信用保険", 450, "東南アジア新規取引先への売掛金リスクヘッジとして取引信用保険を提案。与信管理の社内体制が未整備のため、保険付帯サービスに関心。", "取引先リスト（上位20社）の提出を依頼", "田中営業部長"),
]

shoudan_schema = StructType([
    StructField("商談ID", StringType(), False),
    StructField("顧客ID", StringType(), False),
    StructField("企業名", StringType(), True),
    StructField("商談件名", StringType(), True),
    StructField("商談日", StringType(), True),
    StructField("接触方法", StringType(), True),
    StructField("ステータス", StringType(), True),
    StructField("保険種目", StringType(), True),
    StructField("見込保険料_万円", IntegerType(), True),
    StructField("商談メモ", StringType(), True),
    StructField("次回アクション", StringType(), True),
    StructField("営業担当", StringType(), True),
])

df_shoudan = spark.createDataFrame(shoudan_data, schema=shoudan_schema)
print("=== 商談履歴 ===")
display(df_shoudan)

# COMMAND ----------

# DBTITLE 1,テーブル書き込み
# === テーブルとして保存 ===
df_customers.write.mode("overwrite").saveAsTable(CUSTOMERS)
print(f"✓ 顧客マスター → {CUSTOMERS} ({df_customers.count()} 件)")

df_shoudan.write.mode("overwrite").saveAsTable(SHOUDAN_HISTORY)
print(f"✓ 商談履歴 → {SHOUDAN_HISTORY} ({df_shoudan.count()} 件)")

print(f"\n=== テーブル一覧 ===")
display(spark.sql(f"SHOW TABLES IN {CATALOG}.{SCHEMA}"))

# COMMAND ----------

# DBTITLE 1,データサマリー
from pyspark.sql.functions import sum as _sum

print(f"顧客マスター: {df_customers.count()} 社")
print(f"商談履歴: {df_shoudan.count()} 件")

print(f"\n【ステータス別商談数】")
display(df_shoudan.groupBy("ステータス").count().orderBy("count", ascending=False))

print(f"\n【営業担当別 見込保険料合計（万円）】")
display(df_shoudan.groupBy("営業担当").agg(_sum("見込保険料_万円").alias("見込保険料合計_万円")).orderBy("見込保険料合計_万円", ascending=False))
