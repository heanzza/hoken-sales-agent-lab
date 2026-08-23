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

COMMENT ON TABLE jp_fsi_catalog.houjin_eigyo.shodan_katsudo IS '商談活動履歴。担当企業ごとの訪問・提案・フォロー等の活動記録。memo列には社内用語(深耕/総幹事/GLTD等)が含まれるためshanai_ryakugo(用語集)と併せて解釈する。'

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

-- SPLIT --

COMMENT ON TABLE jp_fsi_catalog.houjin_eigyo.shanai_ryakugo IS '社内略語・業務用語集(グロッサリ)。法人営業で使う略語・KPI・商品区分・チャネルの正式名称と定義。営業メモや質問に登場する用語の解釈に用いる。'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.shanai_ryakugo ALTER COLUMN ryaku COMMENT '略語・用語(例: ANP, 深耕, 総幹事, GLTD, BA)'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.shanai_ryakugo ALTER COLUMN seishiki_meisho COMMENT '正式名称'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.shanai_ryakugo ALTER COLUMN eigo COMMENT '英語表記'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.shanai_ryakugo ALTER COLUMN kubun COMMENT '用語の区分(KPI/商品/チャネル/営業方針/保険用語/業務/部門)'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.shanai_ryakugo ALTER COLUMN teigi COMMENT '定義・意味'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.shanai_ryakugo ALTER COLUMN ruigigo COMMENT '類義語・シノニム'

-- SPLIT --

ALTER TABLE jp_fsi_catalog.houjin_eigyo.shanai_ryakugo ALTER COLUMN owner_bumon COMMENT '所管部門'
