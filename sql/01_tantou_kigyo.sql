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
FROM newtgt n;
