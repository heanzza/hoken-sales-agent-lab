# 法人営業AIエージェント・ラボ — セットアップ一式

生命保険の**法人営業**を題材に、Databricks 上で「営業AIエージェント」を体感する **30分ハンズオン**のデモ環境をセットアップするための一式です。

他社（Snowflake）が提示する営業AI PoCが「営業プロセス①〜⑤の**出力精度**」を測るのに対し、Databricks は論点を **精度の天井を決める Context（用語=Pages・関係=Ontology）／統制（Unity AI Gateway）／本番化（Agent Bricks）** へ移す——という流れを、ビジネスユーザーがノーコード・UI操作だけで体感します。

> ハンズオン進行台本は [`docs/handson.html`](docs/handson.html)（ブラウザで開く）。

---

## 何がセットアップされるか

| 種別 | 内容 | 作成物 |
|---|---|---|
| **利用データ** | 担当企業96社・商談200件・社内用語25語・企業360°ビュー・KPIメトリックビュー | `sql/*.sql` |
| **Pages 投入内容** | 用語・KPI・区分の定義集（Unity Catalog Pages 用） | `pages/houjin_eigyo_pages.md` |
| **Genie Agent** | キュレーション済み「法人営業アシスタント」＋対比用「Before」 | `genie/*.json` |
| **商品資料** | 商品パンフ/約款 PDF 4件（KAのソース） | `product_docs/pdf/*.pdf` |
| **台本** | ファシリテーター用 30分台本（HTML） | `docs/handson.html` |

## 前提

- Databricks CLI v0.292+（認証済みプロファイル）／`jq`／`python3`
- **前提データ**: 法人契約ファクト `houjin_keiyaku` と マスタ `channel_master`/`shohin_master`/`shibu_master` が対象スキーマに存在すること（本ラボの企業/商談/360ビューはこれらに結合します）。無い場合は同等のダミーをご用意ください。
- SQL Warehouse（Serverless 推奨）

## クイックスタート

```bash
# 1) 利用データ（テーブル/ビュー/用語集/Metric View）＋ 商品PDF を作成
PROFILE=<your-profile> ./setup.sh
#   任意: CATALOG=<catalog> SCHEMA=<schema> を上書き可（既定 jp_fsi_catalog.houjin_eigyo）

# 2) Genie Space を2つ作成（本命＋Before）
PROFILE=<your-profile> WAREHOUSE=<warehouse_id> ./genie/create_genie_spaces.sh
#   → 出力された space_id を台本/スライドの接続情報に反映
```

`setup.sh` は `sql/` 内の各SQLを対象カタログ・スキーマに読み替えて実行し、Volume `product_docs` を作成して商品PDFをアップロードします。

## Pages の投入（用語・KPI／Beta）

`pages/houjin_eigyo_pages.md` が Pages に投入する内容です（用語25語・KPI定義・チャネル対応・商品区分・業務定義・Related Assets）。

1. Catalog Explorer → **Discover** → Domain を作成
2. **Pages** で `houjin_eigyo_pages.md` を取り込み
3. Related Assets に `tantou_kigyo` / `houjin_keiyaku` / `shodan_katsudo` / `shanai_ryakugo` / `v_eigyo_360` / `mv_eigyo_kpi` を紐付け

> Pages（旧称ビジネスグロッサリ。現在は Domains＋Pages＋Metric Views＋Certification として semantics/Discover に統合）は Beta です。未有効の場合、本ラボは用語集テーブル `shanai_ryakugo` ＋ Genie の Instructions で同等効果を再現しています。

## Agent Bricks（KA / MAS）— UIで作成（約5分）

CLIでの作成手段がないため UI で作成します。

**① Knowledge Assistant**（AI/BI → Agent Bricks → Knowledge Assistant → Create）
- 名前: `hoken_houjin_product_ka`
- ナレッジソース: Volume `/Volumes/<catalog>/<schema>/product_docs`（PDF 4件）
- 動作確認: 「団体定期保険の最低加入人数は?」→ 原則5名以上／「GLTDの免責期間は?」→ 通常30〜90日

**② Multi-Agent Supervisor**（AI/BI → Agent Bricks → Multi-Agent Supervisor → Create）
- 名前: `hoken_houjin_sales_supervisor`
- エージェント1（データ）: Genie space（本命）
- エージェント2（商品資料）: KA `hoken_houjin_product_ka`
- 動作確認: 「九州建設株式会社向けに、未提案商品をふまえた提案の骨子を作って。付保基準も含めて」

## Unity AI Gateway（利用・コストの可視化）

STEP6 で見せる「支出可視化・帰属」は system tables で確認できます（例）。

```sql
-- エンドポイント別・ユーザー別のトークン利用（直近30日）
SELECT served_entity_id, count(*) AS requests,
       sum(input_token_count)  AS in_tok,
       sum(output_token_count) AS out_tok,
       count(DISTINCT requester) AS users
FROM system.serving.endpoint_usage
WHERE request_time > current_timestamp() - INTERVAL 30 DAYS
GROUP BY served_entity_id ORDER BY requests DESC;

-- 外部モデルの支出
SELECT * FROM system.ai_gateway.external_model_spend ORDER BY 1 DESC LIMIT 50;
```

## 商品PDFの再生成（任意）

同梱の `product_docs/pdf/*.pdf` をそのまま使えます。作り直す場合:

```bash
./product_docs/render.sh   # make_pdfs.py で HTML 生成 → Chrome headless で日本語PDF化
```

> 日本語PDFは ReportLab 等でフォント埋め込みに失敗し文字化けする場合があるため、HTML→PDF（システムのCJKフォント使用）で生成しています。

## ディレクトリ構成

```
.
├── setup.sh                         # 利用データ作成＋PDFアップロード（メイン）
├── sql/                             # テーブル/ビュー/用語集/Metric View
│   ├── 01_tantou_kigyo.sql          #   担当企業プロファイル（既存90+新規開拓6）
│   ├── 02_shodan_katsudo.sql        #   商談活動履歴（社内用語をメモに埋込）
│   ├── 03_shanai_ryakugo.sql        #   社内用語集25語
│   ├── 04_comments_constraints.sql  #   コメント＋PK/FK制約
│   ├── 05_v_eigyo_360.sql           #   企業360°ビュー（契約×商談×未提案）
│   └── 06_mv_eigyo_kpi.sql          #   KPIメトリックビュー
├── genie/
│   ├── genie_agent.json             # 本命（キュレーション済み）
│   ├── genie_before.json            # Before（用語集・文脈なし）
│   └── create_genie_spaces.sh
├── pages/
│   └── houjin_eigyo_pages.md        # Pages 投入用の用語・KPI定義
├── product_docs/
│   ├── pdf/                         # 商品PDF 4件（KAソース）
│   ├── make_pdfs.py                 # PDFのHTML元
│   └── render.sh                    # 再生成スクリプト
└── docs/
    └── handson.html                 # 30分ハンズオン台本
```

## 注記

- 商品資料は架空の「サンプル生命」による営業支援用サンプルです（実在の商品・企業とは無関係）。
- 既存の `houjin_eigyo` デモ資産は変更せず、追加のみで構築する設計です。
- SQL内のカタログ・スキーマ名（既定 `jp_fsi_catalog.houjin_eigyo`）は `setup.sh` / `create_genie_spaces.sh` が指定値へ読み替えます。
