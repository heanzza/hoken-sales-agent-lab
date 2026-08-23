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
FROM gen;
