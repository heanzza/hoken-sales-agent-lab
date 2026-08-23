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
