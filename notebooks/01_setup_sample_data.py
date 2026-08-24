# Databricks notebook source
# MAGIC %md
# MAGIC # 01_setup_sample_data — 利用データのセットアップ
# MAGIC 
# MAGIC 担当企業・商談・企業360°ビュー・KPIメトリックビューを作成します。**［すべて実行］**してください。
# MAGIC 
# MAGIC 社内用語集は SQL テーブルとしては作成しません（**Unity Catalog Pages** で管理し、Genie の Instructions が定義を保持します。`pages/houjin_eigyo_pages.md` 参照）。
# MAGIC 
# MAGIC **前提**: 法人契約ファクト `houjin_keiyaku` とマスタ `channel_master` / `shohin_master` / `shibu_master` が対象スキーマに存在すること。
# COMMAND ----------

# MAGIC %run ./00_config
# COMMAND ----------

# 各SQLは jp_fsi_catalog.houjin_eigyo を対象カタログ・スキーマに置き換えて実行する
_CAT_SCH = f"{catalog}.{schema}"
def run(sql: str):
    spark.sql(sql.replace("jp_fsi_catalog.houjin_eigyo", _CAT_SCH))
def run_multi(sql: str, sep: str = "-- SPLIT --"):
    for s in sql.split(sep):
        s = s.strip().rstrip(";").strip()
        if s:
            run(s)
# COMMAND ----------

# MAGIC %md
# MAGIC ## 担当企業プロファイル (tantou_kigyo)
# COMMAND ----------

run("""
CREATE OR REPLACE TABLE jp_fsi_catalog.houjin_eigyo.tantou_kigyo AS
WITH base AS (
  SELECT DISTINCT kaisha_name FROM jp_fsi_catalog.houjin_eigyo.houjin_keiyaku
),
existing AS (
  SELECT
    kaisha_name,
    CASE
      WHEN kaisha_name LIKE '%電機%' OR kaisha_name LIKE '%電気%' THEN '電機・精密'
      WHEN kaisha_name LIKE '%建設%' THEN '建設'
      WHEN kaisha_name LIKE '%製薬%' THEN '医薬・ヘルスケア'
      WHEN kaisha_name LIKE '%海運%' OR kaisha_name LIKE '%運輸%' OR kaisha_name LIKE '%物流%' THEN '運輸・物流'
      WHEN kaisha_name LIKE '%システム%' OR kaisha_name LIKE '%情報%' OR kaisha_name LIKE '%通信%' THEN '情報通信'
      WHEN kaisha_name LIKE '%商事%' OR kaisha_name LIKE '%商会%' THEN '商社・卸'
      WHEN kaisha_name LIKE '%製作所%' OR kaisha_name LIKE '%工業%' THEN '製造業'
      WHEN kaisha_name LIKE '%銀行%' OR kaisha_name LIKE '%信託%' OR kaisha_name LIKE '%証券%' THEN '金融'
      WHEN kaisha_name LIKE '%電力%' OR kaisha_name LIKE '%エネルギー%' OR kaisha_name LIKE '%ガス%' THEN 'エネルギー'
      ELSE 'サービス'
    END AS gyoshu,
    element_at(array(120, 350, 620, 980, 1500, 2400, 4200, 8000), pmod(hash(kaisha_name), 8) + 1) AS jugyoin_su,
    element_at(array('上場', '上場', '非上場', '非上場', '非上場'), pmod(hash(kaisha_name, 'jojo'), 5) + 1) AS jojo_kubun,
    element_at(array('A', 'A', 'B', 'B', 'B', 'C'), pmod(hash(kaisha_name, 'yoshin'), 6) + 1) AS yoshin_rank,
    element_at(array(
      '直近3期増収・従業員数が前年比8%増',
      '新工場を開設し従業員数が急増中',
      '海外売上比率が拡大・駐在員が増加',
      '株式上場(IPO)を準備中',
      '同業のM&Aを実施し組織を統合中',
      '業績は横ばいだが退職者が増加傾向',
      '大型設備投資で借入が増加',
      '事業承継・世代交代の局面'
    ), pmod(hash(kaisha_name, 'signal'), 8) + 1) AS seicho_signal,
    'kigyo' AS src
  FROM base
),
newtgt AS (
  SELECT * FROM (VALUES
    ('みらいテック株式会社', '情報通信', 480, '非上場', 'B', 'IPO準備中・エンジニアを年間100名採用予定、福利厚生を拡充したい'),
    ('日本グリーンエナジー株式会社', 'エネルギー', 1350, '非上場', 'A', '再エネ事業が急拡大・従業員数が前年比20%増、拠点新設が続く'),
    ('さくら物流サービス株式会社', '運輸・物流', 2600, '上場', 'B', 'EC需要でドライバーを大量採用、労災・就業不能リスクへの備えが課題'),
    ('関西メディカル製薬株式会社', '医薬・ヘルスケア', 720, '上場', 'A', '新薬承認で増収、研究人材の採用競争が激化・退職金制度を見直したい'),
    ('東海フードシステムズ株式会社', 'サービス', 3100, '非上場', 'C', '多店舗展開でパート比率が高い、事業承継を控え経営者保障が手薄'),
    ('北陸精密工業株式会社', '製造業', 950, '非上場', 'B', '海外展開を加速・駐在員が増加、団体保険は未導入')
  ) AS t(kaisha_name, gyoshu, jugyoin_su, jojo_kubun, yoshin_rank, kadai_memo)
)
SELECT
  e.kaisha_name,
  e.gyoshu,
  e.jugyoin_su,
  CAST(round(e.jugyoin_su * element_at(array(0.35, 0.5, 0.8, 1.2), pmod(hash(e.kaisha_name, 'uriage'), 4) + 1), 0) AS INT) AS uriage_oku,
  e.jojo_kubun,
  e.yoshin_rank,
  e.seicho_signal,
  CASE e.gyoshu
    WHEN '情報通信' THEN '人材採用と定着が最重要。エンジニアの福利厚生・就業不能保障の強化ニーズ'
    WHEN '製造業' THEN '現場の労災・就業不能リスクと退職金原資の準備が課題'
    WHEN '医薬・ヘルスケア' THEN '研究人材の採用競争。退職金・企業年金の水準見直しニーズ'
    WHEN '運輸・物流' THEN 'ドライバーの労災・就業不能リスクへの備えが最重要'
    WHEN 'エネルギー' THEN '大型設備投資に伴う経営者保障と従業員福利厚生の両立'
    WHEN '建設' THEN '現場労災と事業承継対策。経営者保険の見直しニーズ'
    WHEN '金融' THEN '福利厚生の競争力維持と退職金制度の最適化'
    ELSE '福利厚生の拡充と経営者の事業保障が主な検討テーマ'
  END AS kadai_memo,
  '既存' AS kubun
FROM existing e
UNION ALL
SELECT
  n.kaisha_name, n.gyoshu, n.jugyoin_su,
  CAST(round(n.jugyoin_su * 0.7, 0) AS INT) AS uriage_oku,
  n.jojo_kubun, n.yoshin_rank,
  n.kadai_memo AS seicho_signal,
  n.kadai_memo,
  '新規開拓' AS kubun
FROM newtgt n
""")
# COMMAND ----------

# MAGIC %md
# MAGIC ## 商談活動履歴 (shodan_katsudo)
# COMMAND ----------

run("""
CREATE OR REPLACE TABLE jp_fsi_catalog.houjin_eigyo.shodan_katsudo AS
WITH gen AS (
  SELECT
    k.kaisha_name,
    k.gyoshu,
    k.kubun,
    explode(sequence(1, pmod(hash(k.kaisha_name, 'cnt'), 3) + 1)) AS seq
  FROM jp_fsi_catalog.houjin_eigyo.tantou_kigyo k
)
SELECT
  concat('SD', lpad(CAST(row_number() OVER (ORDER BY kaisha_name, seq) AS STRING), 5, '0')) AS shodan_id,
  kaisha_name,
  date_add(DATE'2026-06-30', -1 * pmod(hash(kaisha_name, seq, 'day'), 120)) AS katsudo_date,
  element_at(array('初回訪問', 'ヒアリング', '提案', 'クロージング', 'フォロー'),
             pmod(hash(kaisha_name, seq, 'stage'), 5) + 1) AS stage,
  element_at(array('団体定期保険', '従業員福利厚生プラン', '経営者向け定期保険', '退職金準備プラン', '法人向け医療保険', '事業保障プラン'),
             pmod(hash(kaisha_name, seq, 'prod'), 6) + 1) AS kanshin_shohin,
  element_at(array(
    '深耕方針で既存契約先を訪問。総幹事の獲得余地を確認した。',
    '新規開拓ターゲットとして初回接触。人事部長に福利厚生ニーズをヒアリング。',
    'GLTD(団体長期障害所得補償)の導入を提案。就業不能リスクへの関心が高い。',
    '被保険者数の増加に伴い団体定期の付保内容を見直したいとの要望。',
    '事業承継を見据えた経営者保険を提案。予定利率と解約返戻金を説明。',
    '退職金原資の準備として企業年金プランを提示。ANP拡大の好機。',
    '既存の団体扱契約の継続率(13ヶ月継続率)を確認。解約防止のフォロー実施。'
  ), pmod(hash(kaisha_name, seq, 'memo'), 7) + 1) AS memo,
  element_at(array(
    '次回、役員向けに提案書を提示',
    '人事部へ見積もりを提出',
    '他社比較資料を準備し再訪',
    '経理部と保険料の予算感をすり合わせ',
    '契約更改のタイミングで再提案',
    'クロージングに向け条件を最終調整'
  ), pmod(hash(kaisha_name, seq, 'next'), 6) + 1) AS next_action,
  element_at(array('高橋由美', '田中健', '佐藤花子', '伊藤愛', '中村美咲', '渡辺翔', '山本さゆり', '小林大輔'),
             pmod(hash(kaisha_name), 8) + 1) AS tanto
FROM gen
""")
# COMMAND ----------

# MAGIC %md
# MAGIC ## コメント & PK/FK 制約
# COMMAND ----------

run_multi("""
COMMENT ON TABLE jp_fsi_catalog.houjin_eigyo.tantou_kigyo IS '担当企業プロファイル。法人営業が担当する企業(既存契約先90社+新規開拓ターゲット6社)の業種・規模・成長シグナル・想定課題。kaisha_nameでhoujin_keiyaku(契約実績)およびshodan_katsudo(商談履歴)と結合する。'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.tantou_kigyo ALTER COLUMN kaisha_name COMMENT '会社名。契約・商談テーブルとの結合キー'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.tantou_kigyo ALTER COLUMN gyoshu COMMENT '業種'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.tantou_kigyo ALTER COLUMN jugyoin_su COMMENT '従業員数(人)。団体保険の被保険者規模の目安'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.tantou_kigyo ALTER COLUMN uriage_oku COMMENT '年間売上高(億円)'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.tantou_kigyo ALTER COLUMN jojo_kubun COMMENT '上場/非上場の区分'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.tantou_kigyo ALTER COLUMN yoshin_rank COMMENT '与信区分(A/B/C)。取引先の信用力'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.tantou_kigyo ALTER COLUMN seicho_signal COMMENT '成長シグナル。増収・採用増・拠点新設・IPO準備など営業アプローチのきっかけとなる変化'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.tantou_kigyo ALTER COLUMN kadai_memo COMMENT '想定課題メモ。営業が仮説立てするための企業課題'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.tantou_kigyo ALTER COLUMN kubun COMMENT '既存(契約あり)か新規開拓ターゲットかの区分'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.tantou_kigyo ALTER COLUMN kaisha_name SET NOT NULL

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.tantou_kigyo ADD CONSTRAINT pk_tantou_kigyo PRIMARY KEY (kaisha_name)

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.shodan_katsudo ALTER COLUMN kaisha_name COMMENT '会社名。tantou_kigyoとの結合キー'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.shodan_katsudo ALTER COLUMN katsudo_date COMMENT '商談・活動の実施日'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.shodan_katsudo ALTER COLUMN stage COMMENT '商談ステージ(初回訪問/ヒアリング/提案/クロージング/フォロー)'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.shodan_katsudo ALTER COLUMN kanshin_shohin COMMENT '関心商品。顧客が興味を示している商品'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.shodan_katsudo ALTER COLUMN memo COMMENT '商談メモ。社内用語を含む活動内容の記録'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.shodan_katsudo ALTER COLUMN next_action COMMENT '次アクション'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.shodan_katsudo ALTER COLUMN tanto COMMENT '担当営業'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.shodan_katsudo ALTER COLUMN shodan_id SET NOT NULL

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.shodan_katsudo ADD CONSTRAINT pk_shodan PRIMARY KEY (shodan_id)

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.shodan_katsudo ADD CONSTRAINT fk_shodan_kigyo FOREIGN KEY (kaisha_name) REFERENCES jp_fsi_catalog.houjin_eigyo.tantou_kigyo(kaisha_name)
""")
# COMMAND ----------

# MAGIC %md
# MAGIC ## 企業360°ビュー (v_eigyo_360)
# COMMAND ----------

run("""
CREATE OR REPLACE VIEW jp_fsi_catalog.houjin_eigyo.v_eigyo_360 AS
WITH held AS (
  SELECT
    kaisha_name,
    collect_set(shohin_code) AS codes,
    count(*) AS keiyaku_su,
    sum(CASE WHEN status IN ('継続','成約') THEN 1 ELSE 0 END) AS yuko_keiyaku_su,
    CAST(round(sum(CASE WHEN status IN ('継続','成約') THEN CAST(anp AS DOUBLE) ELSE 0 END) / 10000, 0) AS INT) AS hoyu_anp_manyen,
    round(avg(CAST(keizoku_ritsu_13m AS DOUBLE)), 3) AS avg_13m_keizoku_ritsu
  FROM jp_fsi_catalog.houjin_eigyo.houjin_keiyaku
  GROUP BY kaisha_name
),
gap AS (
  SELECT
    k.kaisha_name,
    array_join(
      collect_list(CASE WHEN NOT array_contains(coalesce(h.codes, array()), s.shohin_code) THEN s.shohin_name END),
      '、'
    ) AS mihyo_shohin
  FROM jp_fsi_catalog.houjin_eigyo.tantou_kigyo k
  CROSS JOIN jp_fsi_catalog.houjin_eigyo.shohin_master s
  LEFT JOIN held h ON k.kaisha_name = h.kaisha_name
  GROUP BY k.kaisha_name
),
act AS (
  SELECT kaisha_name, count(*) AS shodan_su, max(katsudo_date) AS saishu_shodan_bi
  FROM jp_fsi_catalog.houjin_eigyo.shodan_katsudo
  GROUP BY kaisha_name
),
latest AS (
  SELECT kaisha_name, stage AS chikin_stage, memo AS chikin_memo, next_action AS chikin_next_action, tanto
  FROM (
    SELECT *, row_number() OVER (PARTITION BY kaisha_name ORDER BY katsudo_date DESC, shodan_id DESC) AS rn
    FROM jp_fsi_catalog.houjin_eigyo.shodan_katsudo
  ) WHERE rn = 1
)
SELECT
  k.kaisha_name,
  k.kubun,
  k.gyoshu,
  k.jugyoin_su,
  k.uriage_oku,
  k.jojo_kubun,
  k.yoshin_rank,
  k.seicho_signal,
  k.kadai_memo,
  coalesce(h.keiyaku_su, 0) AS keiyaku_su,
  coalesce(h.yuko_keiyaku_su, 0) AS yuko_keiyaku_su,
  coalesce(h.hoyu_anp_manyen, 0) AS hoyu_anp_manyen,
  h.avg_13m_keizoku_ritsu,
  g.mihyo_shohin,
  coalesce(a.shodan_su, 0) AS shodan_su,
  a.saishu_shodan_bi,
  l.chikin_stage,
  l.chikin_memo,
  l.chikin_next_action,
  l.tanto
FROM jp_fsi_catalog.houjin_eigyo.tantou_kigyo k
LEFT JOIN held h ON k.kaisha_name = h.kaisha_name
LEFT JOIN gap g ON k.kaisha_name = g.kaisha_name
LEFT JOIN act a ON k.kaisha_name = a.kaisha_name
LEFT JOIN latest l ON k.kaisha_name = l.kaisha_name
""")
# COMMAND ----------

# MAGIC %md
# MAGIC ## KPIメトリックビュー (mv_eigyo_kpi)
# COMMAND ----------

run_multi("""
CREATE OR REPLACE VIEW jp_fsi_catalog.houjin_eigyo.v_keiyaku_enriched AS
SELECT
  k.keiyaku_id,
  k.kaisha_name,
  k.gyoshu,
  CAST(k.anp AS DOUBLE) AS anp,
  CAST(k.keizoku_ritsu_13m AS DOUBLE) AS keizoku_ritsu_13m,
  CAST(k.hihokensha_su AS INT) AS hihokensha_su,
  k.status,
  k.tanto,
  k.keiyaku_date,
  date_trunc('MONTH', k.keiyaku_date) AS keiyaku_month,
  c.channel_name,
  s.shohin_kubun,
  s.shohin_name,
  b.shibu_name,
  b.region
FROM jp_fsi_catalog.houjin_eigyo.houjin_keiyaku k
LEFT JOIN jp_fsi_catalog.houjin_eigyo.channel_master c ON k.channel_code = c.channel_code
LEFT JOIN jp_fsi_catalog.houjin_eigyo.shohin_master s ON k.shohin_code = s.shohin_code
LEFT JOIN jp_fsi_catalog.houjin_eigyo.shibu_master b ON k.shibu_code = b.shibu_code

-- SPLIT --

CREATE OR REPLACE VIEW jp_fsi_catalog.houjin_eigyo.mv_eigyo_kpi
WITH METRICS
LANGUAGE YAML
AS $$
version: 1.1
source: jp_fsi_catalog.houjin_eigyo.v_keiyaku_enriched
comment: "法人営業KPIメトリックビュー。ANP合計・契約件数・平均13ヶ月継続率を、チャネル/業種/商品/支社/契約月で集計。"
dimensions: [{name: channel, expr: channel_name}, {name: gyoshu, expr: gyoshu}, {name: shohin_kubun, expr: shohin_kubun}, {name: shohin_name, expr: shohin_name}, {name: region, expr: region}, {name: shibu, expr: shibu_name}, {name: status, expr: status}, {name: keiyaku_month, expr: keiyaku_month}]
measures: [{name: total_anp, expr: SUM(anp)}, {name: keiyaku_kensu, expr: COUNT(1)}, {name: avg_13m_ritsu, expr: AVG(keizoku_ritsu_13m)}]
$$
""")
# COMMAND ----------

# MAGIC %md
# MAGIC ## 確認
# COMMAND ----------

display(spark.sql(f"""
SELECT 'tantou_kigyo' AS t, count(*) n FROM {catalog}.{schema}.tantou_kigyo
UNION ALL SELECT 'shodan_katsudo', count(*) FROM {catalog}.{schema}.shodan_katsudo
UNION ALL SELECT 'v_eigyo_360',    count(*) FROM {catalog}.{schema}.v_eigyo_360
"""))
# COMMAND ----------

display(spark.sql(f"""
SELECT kaisha_name, gyoshu, jugyoin_su, hoyu_anp_manyen, mihyo_shohin
FROM {catalog}.{schema}.v_eigyo_360
WHERE kubun = '既存' AND mihyo_shohin <> ''
ORDER BY hoyu_anp_manyen DESC LIMIT 10
"""))
