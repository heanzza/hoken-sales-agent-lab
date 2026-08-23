# 法人営業 用語・KPI（Unity Catalog Pages 投入用）

このドキュメントは、Unity Catalog **Pages**（旧称: ビジネスグロッサリ。現在は Domains＋Pages＋Metric Views＋Certification として semantics/Discover に統合）へ投入する、法人営業ドメインの**用語・KPI・区分**の定義集です。

Pages に取り込むことで、Genie / データ探索が社内用語を正しく解釈し、回答精度の天井が上がります（ハンズオン STEP2 の「Context」に対応）。本ハンズオンでは、この内容を用語集テーブル `shanai_ryakugo` ＋ Genie の Instructions として実装し、同等の効果を再現しています。

- **対象スキーマ**: `jp_fsi_catalog.houjin_eigyo`（環境に合わせて読み替え）
- **Pages 投入手順**: Catalog Explorer → Discover → Domain 作成 → Pages でこのドキュメントを取り込み → Related Assets に下記テーブル/ビューを紐付け

---

## 1. 社内用語・略語

| 用語 | 正式名称 | 英語 | 区分 | 定義 | 類義語 | 所管 |
|---|---|---|---|---|---|---|
| ANP | 年換算保険料 | Annualized New Premium | KPI | 新契約の保険料を年額に換算した指標。法人営業の主要な成績KPI。 | 年換算保険料 | 法人営業企画部 |
| 13ヶ月継続率 | 十三ヶ月継続率 | 13-month persistency | KPI | 契約から13ヶ月後に有効に継続している契約の割合。契約の品質指標。 | 継続率, persistency | 法人営業企画部 |
| 団定 | 団体定期保険 | Group Term Life | 商品 | 企業が従業員を一括して被保険者とする1年更新の定期保険。 | 団体定期 | 商品部 |
| 団体扱 | 団体扱契約 | Group-billed policy | チャネル | 企業経由で保険料を給与天引き等でまとめて収納する契約形態。 | だんたいあつかい | 法人営業企画部 |
| 総幹事 | 総幹事会社 | Lead insurer | 業務 | 複数保険会社が共同引受する団体保険で契約事務を統括する幹事会社。獲得すると取引の主導権を握れる。 | 幹事 | 法人営業企画部 |
| GLTD | 団体長期障害所得補償保険 | Group Long Term Disability | 商品 | 従業員が就業不能になった際に所得を長期にわたり補償する団体保険。 | 就業不能保障 | 商品部 |
| 深耕 | 深耕開拓 | Account deepening | 営業方針 | 既存の契約先に追加提案を行いシェアを高める営業活動。 | アップセル, クロスセル | 法人営業企画部 |
| 新規開拓 | 新規開拓 | New business acquisition | 営業方針 | まだ取引のない企業を新たに開拓する営業活動。 | new logo, 新規 | 法人営業企画部 |
| 事保 | 事業保障 | Business protection | 商品区分 | 経営者の死亡・就業不能時に事業を守るための保険。 | 事業保障プラン | 商品部 |
| 経営者保険 | 経営者保険 | Keyman insurance | 商品区分 | 経営者・役員を被保険者とし事業保障や退職金準備に用いる保険。 | キーマン保険 | 商品部 |
| 福利厚生 | 福利厚生プラン | Employee benefits | 商品区分 | 従業員向けの保障・退職金等の福利厚生制度。 | ベネフィット | 商品部 |
| 退準 | 退職金準備 | Retirement funding | 商品区分 | 従業員・役員の退職金原資を準備する保険・年金プラン。 | 退職金原資 | 商品部 |
| 予定利率 | 予定利率 | Assumed interest rate | 保険用語 | 保険会社が保険料算出時に見込む運用利回り。解約返戻金の水準に影響する。 |  | 商品部 |
| 解約返戻金 | 解約返戻金 | Surrender value | 保険用語 | 契約を解約した際に契約者へ払い戻される金額。 | 返戻金 | 商品部 |
| 被保険者 | 被保険者 | Insured person | 保険用語 | 保険の対象となる人。団体保険では加入する従業員を指す。 |  | 商品部 |
| 付保 | 付保 | Coverage placement | 業務 | 保険をかけること。付保内容=保障の設計内容を指す。 |  | 商品部 |
| BA | 銀行窓口販売 | Bancassurance | チャネル | 銀行の窓口を通じて保険を販売するチャネル。 | 銀窓, バンカシュアランス | 代理店営業企画部 |
| 代企 | 代理店営業企画 | Agency channel planning | チャネル | 代理店経由の営業を企画・支援するチャネル。 | 代理店チャネル | 代理店営業企画部 |
| 法企 | 法人営業企画部 | Corporate sales planning dept. | 部門 | 法人向け営業を統括・企画する部門。 | 法人営業企画部 | 法人営業企画部 |
| 直販 | 直接販売 | Direct sales | チャネル | 自社の営業職員が企業に直接販売するチャネル。 | ダイレクト | 法人営業企画部 |
| DB | 確定給付企業年金 | Defined Benefit | 商品区分 | 給付額があらかじめ定められた企業年金制度。 | 確定給付 | 商品部 |
| DC | 確定拠出年金 | Defined Contribution | 商品区分 | 掛金が確定し運用成果で将来の給付が変わる企業年金制度（企業型DC）。 | 確定拠出, 401k | 商品部 |
| クロスセル | 交差販売 | Cross-sell | 営業方針 | 既存の契約先に別の商品を追加提案すること。深耕の代表的な手法。 | 追加提案 | 法人営業企画部 |
| 与信 | 与信区分 | Credit rating | 業務 | 取引先企業の信用力の区分（A/B/C）。提案の可否や条件に影響する。 | 信用格付 | 法人営業企画部 |
| パイプライン | 商談パイプライン | Sales pipeline | 業務 | 進行中の商談を段階別に管理した見込み案件の総体。 | 見込み案件 | 法人営業企画部 |

---

## 2. KPI・指標定義（Metric View: `mv_eigyo_kpi`）

| 指標 | 定義 | 計算 |
|---|---|---|
| ANP合計 (total_anp) | 年換算保険料の合計 | `SUM(anp)` |
| 契約件数 (keiyaku_kensu) | 契約の件数 | `COUNT(1)` |
| 平均13ヶ月継続率 (avg_13m_ritsu) | 13ヶ月継続率の平均 | `AVG(keizoku_ritsu_13m)` |
| 保有ANP（万円） | 有効契約（継続・成約）の年換算保険料合計（万円） | `SUM(anp WHERE status IN ('継続','成約'))/10000`（`v_eigyo_360.hoyu_anp_manyen`） |

**集計軸（ディメンション）**: チャネル（channel）／業種（gyoshu）／商品区分（shohin_kubun）／商品名（shohin_name）／地域（region）／支社（shibu）／契約ステータス（status）／契約月（keiyaku_month）

---

## 3. チャネル対応表

| 略語 | チャネル名（データ値） |
|---|---|
| BA | 銀行窓口販売 |
| 代企 | 代理店営業企画経由 |
| 直販 | 直接販売 |
| 団体扱 | 団体扱契約 |
| 法企 | 法人営業企画部直轄 |

## 4. 契約ステータス

| 値 | 意味 |
|---|---|
| 継続 | 有効（継続中） |
| 成約 | 有効（新規成約） |
| 失効 | 失効 |
| 解約 | 解約 |

有効契約は `status IN ('継続','成約')`。

## 5. 商品マスタ（`shohin_master`）

| コード | 商品区分 | 商品名 |
|---|---|---|
| P01 | 経営者保険 | 経営者向け定期保険 |
| P02 | 事保 | 事業保障プラン |
| P03 | 団定 | 団体定期保険 |
| P04 | 福利厚生 | 従業員福利厚生プラン |
| P05 | 法人医療 | 法人向け医療保険 |
| P06 | 退準 | 退職金準備プラン |

---

## 6. 主要な業務定義（営業ロジック）

- **深耕対象**: 既存契約先（`kubun='既存'`）で、未提案商品（`v_eigyo_360.mihyo_shohin`）がある企業。クロスセルの候補。
- **新規開拓ターゲット**: `kubun='新規開拓'` の企業。契約がなく、成長シグナル（`seicho_signal`）を手掛かりにアプローチする。
- **未提案商品**: その企業がまだ契約していない商品（全商品 − 保有商品）。提案の切り口。

## 7. Related Assets（Pages に紐付けるUC資産）

- `jp_fsi_catalog.houjin_eigyo.tantou_kigyo` — 担当企業プロファイル
- `jp_fsi_catalog.houjin_eigyo.houjin_keiyaku` — 法人契約実績
- `jp_fsi_catalog.houjin_eigyo.shodan_katsudo` — 商談活動履歴
- `jp_fsi_catalog.houjin_eigyo.shanai_ryakugo` — 社内用語集
- `jp_fsi_catalog.houjin_eigyo.v_eigyo_360` — 企業360°ビュー
- `jp_fsi_catalog.houjin_eigyo.mv_eigyo_kpi` — KPIメトリックビュー
- `jp_fsi_catalog.houjin_eigyo.shohin_master` — 商品マスタ
