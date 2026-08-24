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
LEFT JOIN latest l ON k.kaisha_name = l.kaisha_name;
