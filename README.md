# 法人営業AIエージェント・ラボ — セットアップ一式

保険会社の**法人営業**を題材に、Databricks 上で「営業AIエージェント」を体感する **30分ハンズオン**のデモ環境をセットアップするための一式です。

他社（Snowflake）が提示する営業AI PoCが「営業プロセスの**出力精度**」を測るのに対し、Databricks は論点を **精度の天井を決める Context（用語=Pages・関係=Ontology）／統制（Unity AI Gateway）／本番化（Agent Bricks）** へ移す——という流れを、ビジネスユーザーがノーコード・UI操作だけで体感します。

> **⚠️ 移行中のお知らせ**
> サンプルデータを、自己完結型の**損害保険（企業向け損保）モデル**（`customers` 顧客マスター＋`shoudan_history` 商談履歴）に刷新しました。
> **`genie/` / `pages/` / `docs/handson.html` / 商品PDF・スライドは、旧モデル（生保・団体保険）を前提に作られており、現在この新サンプルデータと不整合です。** これらの新モデルへの改訂は次ステップで対応します。

---

## サンプルデータ（現行）

自己完結型（外部テーブルへの依存なし）。`notebooks/01_setup_sample_data` を実行して作成します。

| テーブル | 内容 | 件数 |
|---|---|---|
| `customers` | 顧客マスター（担当企業）。顧客ID・企業名・業種・所在地・代表者/担当者・従業員数・年間売上（億円）・顧客ランク(S/A/B/C)・営業担当 等 | 10社 |
| `shoudan_history` | 商談履歴。商談ID・顧客ID・商談件名・商談日・接触方法・ステータス・保険種目・見込保険料（万円）・商談メモ・次回アクション・営業担当 | 15件 |

保険種目は企業向け損保が中心（企業総合保険、サイバーリスク保険、D&O、PL保険、貨物保険、建設工事保険、労災上乗せ 等）。

## 前提

- Serverless SQL Warehouse か DBR 14.3+ のクラスター
- 対象カタログへの `CREATE SCHEMA`／`CREATE TABLE` 権限（カタログ作成は任意。権限が無い場合は既存カタログを使用）
- （任意）ノートブック取り込みを CLI で自動化する場合: Databricks CLI v0.292+／`python3`

## クイックスタート

セットアップは **ノートブック** で行います。

- `notebooks/00_config` … カタログ/スキーマの共通変数（`CATALOG` / `SCHEMA` の2行だけ変更）
- `notebooks/01_setup_sample_data` … `%run ./00_config` の後、`customers` / `shoudan_history` を `createDataFrame` ＋ `saveAsTable` で作成

**手順**: 上記2ファイルをワークスペースにインポート → `01_setup_sample_data` を開いて **［すべて実行］**。

CLI で取り込みを自動化する場合:

```bash
PROFILE=<your-profile> ./setup.sh
#   → notebooks/ をワークスペースにインポート（＋商品PDFがあれば Volume にアップロード）
#   任意: CATALOG=<catalog> SCHEMA=<schema> WORKSPACE_DIR=<path> を上書き可（既定 handson.hoken_sales）
```

## ディレクトリ構成

```
.
├── notebooks/                       # ★ ワークスペースで実行するセットアップ
│   ├── 00_config.py                 #   カタログ/スキーマ共通変数（副作用なし）
│   └── 01_setup_sample_data.py      #   customers / shoudan_history を作成
├── setup.sh                         # 補助: notebooks/ を取込（任意）
├── genie/                           # ⚠️ 旧モデル基準（要改訂）
├── pages/                           # ⚠️ 旧モデル基準の用語・KPI定義（要改訂）
├── product_docs/                    # ⚠️ 旧モデル（生保）商品PDF（要改訂）
└── docs/
    └── handson.html                 # ⚠️ 旧モデル基準の30分台本（要改訂）
```

## 旧モデル資産について（要改訂）

`genie/`（Genie Agent 定義）・`pages/houjin_eigyo_pages.md`（用語集）・`product_docs/`（商品PDF）・`docs/handson.html`（台本）・スライドは、旧サンプルデータ（生保・団体保険：企業契約実績＋社内用語集＋企業360°ビュー）を前提としています。

上記の新サンプルデータ（損保：`customers` / `shoudan_history`）に合わせて、Genie Agent・用語集(Pages)・台本・スライドを作り直す作業は次ステップで対応します。

## 注記

- サンプルデータは架空の企業・商談です（実在の企業・人物とは無関係）。
- カタログ・スキーマ名は `notebooks/00_config` の `CATALOG` / `SCHEMA`（既定 `handson.hoken_sales`）で切り替えます。
