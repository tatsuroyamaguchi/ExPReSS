### ExPReSS

Expert Panel Report Support System

ExPReSSは、がん遺伝子パネル検査におけるエキスパートパネルレポートサポートシステム（ExPReSS）です。このツールは、ゲノムデータ（JSON/XML）を処理し、Excel形式のレポートやProteinPaintおよびDisco用のデータを生成します。Streamlitを利用したWebインターフェースを通じて、ユーザーはデータをアップロードし、結果をダウンロードできます。

---
#### What's New
- version 0.3
  - DataExtractor for CGP搭載
  - SummaryViewer for F1搭載
  - VariantAnnotator搭載
- version 0.2
  - HemeSightに対応

---
#### 対象パネル

- FoundationOne CDx (XML)
- FoundationOne Liquid CDx (XML)
- GenMineTOP (XML)
- Guardant360 CDx (XLSX)
- HemeSight (JSON)
- HemeSight FastTrack (PDF)

---
#### 機能

- ゲノムデータ（JSON/XML）を読み込み、Excelレポートを生成
- ClinVar、ClinGen、GeneBe、TOMMOなどのデータベースから情報を取得
- ProteinPaintおよびDisco用のTSVファイルを生成（HemeSightのみ）
- 生成されたファイルを個別またはZIP形式でダウンロード可能
- Dockerを使用したデプロイ対応

---
#### 必要条件

- Docker（コンテナ化されたデプロイ用）
- Python 3.11以上（ローカル実行の場合）
- 必要なデータファイル（詳細は「データファイル」セクションを参照）

---
#### セットアップ手順

##### 1. リポジトリのクローン

```bash
git clone https://github.com/tatsuroyamaguchi/ExPReSS.git
cd ExPReSS
```
---
##### 2.1. データファイルの準備

以下のファイルを各ディレクトリに配置してください：
- template
  - Template_Hemesight.xlsx: HemeSightテンプレートファイル
  - Template_FastTrack.xlsx: Fast-Track用Excelテンプレートファイル
  - Template_FoundationOne.xlsx: FoundationOneテンプレートファイル
  - Template_GenMineTOP.xlsx: GenMineTOPテンプレート
  - Template_Guardant360.xlsx: Guardant360テンプレート
  - Logo.png: レポートに挿入するロゴ画像
- db
  - JSH_Guidelines.csv: 日本血液学会ガイドライン (http://www.jshem.or.jp/genomgl/home.html) （GitHub内にアップロード済み）
  - pgpv.csv: 小杉班二次的所見より作成 （GitHub内にアップロード済み）


  - Cosmic_CancerGeneCensus_v\*_GRCh38.tsv: CancerGeneCensus (https://cancer.sanger.ac.uk/cosmic/download/cosmic   Cancer Gene Census > Cosmic_CancerGeneCensus_Tsv_v\*_GRCh38.tar > Download in browser)
  - CancerMutationCensus_AllData_Tsv_v\*_GRCh37.tsv.gz: CancerGeneCensus (https://cancer.sanger.ac.uk/cosmic/download/cosmic   Cancer Mutation Census > CancerMutationCensus_AllData_Tsv_v\*_GRCh37.tar > Download in browser)
  - MutationView_r21.csv: The TP53 Database (https://tp53.cancer.gov/static/data/MutationView_r21.csv)
  - erepo-tabbed.tsv: ClinGen (https://erepo.clinicalgenome.org/evrepo/   Download > Tab-delimited)
  - nightly-FeatureSummaries.tsv: CiVIC (https://civicdb.org/releases/main nightly Features TSVをDownload)
  - protein-coding_gene.tsv: HGNC (https://www.genenames.org/download/statistics-and-files/ tsv形式でDownload)


---
##### 2.2. データファイルの圧縮
- CancerMutationCensus_conversion.ipynbを実行: CancerMutationCensus_AllData_Tsv_v*_GRCh37.tsv.gzのデータサイズを圧縮

```python:CancerMutationCensus_conversion.ipynb
# CancerMutationCensus_conversion.ipynb

import pandas as pd
import glob
import os

input_pattern = "CancerMutationCensus_AllData_v*_GRCh37.tsv.gz"
input_files = glob.glob(input_pattern)
input_file = input_files[0]

base_name = os.path.splitext(os.path.splitext(input_file)[0])[0]
output_file = base_name + "_va.tsv.gz"

columns_to_extract = [
    "GENE_NAME",
    "Mutation CDS",
    "COSMIC_SAMPLE_TESTED",
    "COSMIC_SAMPLE_MUTATED",
    "Mutation AA"
]
df = pd.read_csv(input_file, sep="\t", compression="gzip", usecols=columns_to_extract)
df.to_csv(output_file, sep="\t", index=False, compression="gzip")
```

---
##### 3. 初期設定

app/config.pyで初期設定をしてください
- 正常サンプル：口腔粘膜、爪、その他 -> HemeSightのみ
- EP実施医療機関
- 診療科
- EP実施責任者
- 問い合わせ窓口（住所）
- 問い合わせ窓口（電話番号）

---
##### 4. Dockerを使用したビルドと実行

Dockerイメージをビルド:
```bash
docker build -t express .
```

Dockerコンテナを実行:
```bash
docker run --name ExPReSS -p 8503:8503 express
```

ブラウザで http://localhost:8503 にアクセスしてアプリケーションを確認。

---
##### 5. ローカルでの実行（オプション）

Dockerを使用せずローカルで実行する場合：

依存関係をインストール:
```bash
pip install -r requirements.txt
```

アプリケーションを起動:
```bash
cd docker
streamlit run app/ExPReSS.py --server.port 8080
```

ブラウザで http://localhost:8080 にアクセス。

---
#### 使用方法

##### GeneBe API
- GeneBeでAPI Keyを取得
- 詳細はGeneBeのWebサイトで確認  https://genebe.net/about/api
- 以下のコードで認証を確認
```bash
genebe account --username your_username --api-key your_api_key
```

1. Streamlitインターフェースにアクセス
2. サイドバーのSettingを確認
3. 解析ファイルをアップロード
4. 「Run」ボタンをクリックして処理を開始。
5. 生成されたExcelファイルをダウンロード。

---
#### 可視化 (HemeSight)
1. 生成されたファイル（Excel、ProteinPaint TSV、Disco TSV）を個別にまたはZIP形式でダウンロード。
2. ProteinPaintで可視化　https://proteinpaint.stjude.org/


---
#### ディレクトリ構成

```
ExPReSS/
├── Readme.md               # Readme
├── Dockerfile              # Dockerビルド用
├── requirements.txt        # Python依存関係リスト
|
├── app/
│   ├── __init__.py               # 初期化
│   ├── main.py                   # メインスクリプト
│   ├── config.py                 # 設定ファイル
|   |
│   ├── pages/
│   │   ├── DataExtracter_for_CGP.py              # Extractor for CGP Data
│   │   ├── DataViewer.py                         # Data Viewer
│   │   ├── SummaryViewer_for_F1.py               # SummaryViewer for FoudantionOne
│   │   └── VariantAnnotator.py                   # VariantAnnotator
│   │
│   ├── utils/
│   │   ├── __init__.py                            # 初期化
│   │   ├── data_processing.py                     # データ処理
│   │   ├── excel_handling.py                      # Excel操作
│   │   ├── file_handling.py                       # ファイル操作
│   │   ├── link_generator.py                      # Link作成
│   │   ├── parameter.py                           # パラメーター
│   │   ├── sidebar_inputs.py                      # サイドバー
│   │   └── web_scraping.py                        # Webスクレイピング
|   |
|   └── annotator/
|   |   ├── data_fetch.py                          # Webスクレイピング
|   |   ├── link_generator.py                      # Link作成
│   │   ├── parameter.py                           # パラメーター
|   |   ├── parser.py                              # ファイル読み込み
|   |   ├── sidebar.py                             # サイドバー
|   |   └── variant_processor.py                   # データ処理
|   |
|   ├── template/
|   |   ├── Template_HemeSight.xlsx                # HemeSightテンプレート
|   |   ├── Template_FastTrack.xlsx                # HemeSight_FastTrackテンプレート
|   |   ├── Template_FoundationOne.xlsx            # FoundationOneテンプレート
|   |   ├── Template_GenMineTOP.xlsx               # GenMineTOPテンプレート
|   |   ├── Template_Guardant360.xlsx              # Guardant360テンプレート
|   |   └── Logo.png                               # ロゴ画像
|   |
|   └── db/
|       ├── Cosmic_CancerGeneCensus_v*_GRCh38.tsv  # Cancer_in_Roleデータ
|       ├── JSH_Guidelines.csv                     # JSHガイドラインデータ
|       ├── MutationView_r21.csv                   # TP53データ
|       ├── erepo-tabbed.tsv                       # ClinGenデータ
|       |── nightly-FeatureSummaries.tsv           # CiVICデータ
|       |── protein-coding_gene.tsv                # HGNCデータ
|       |── pgpv.csv                               # 小杉班PGPVデータ
|       ├── CancerMutationCensus_AllData_v*_GRCh37.tsv.gz  # COSMICデータ（gzipファイルのまま）
|       └── CancerMutationCensus_compressor.ipynb  # COSMICデータ圧縮プログラム
|
├── img/
│   ├── img_1.png                 # サンプル画面
│   ├── img_2.png                 # サンプルレポート
│   ├── img_3.png                 # サンプルレポート

```

---
#### サンプル画面

![Image_1](./img/img_1.png)

![Image_2](./img/img_2.png)

![Image_3](./img/img_3.png)

---
#### 注意点

- Webスクレイピングは外部サイトに依存するため、ネットワーク接続が必要です。
- 大きなデータセットを処理する場合は、十分なメモリとディスク容量を確保してください。

---
#### 貢献

バグ報告や機能追加の提案は、GitHubのIssuesまたはPull Requestsを通じてお願いします。

---
#### 免責事項

本プログラムのソースコードの著作権は山口達郎に帰属しますが、正確性、完全性、有効性、信頼性、安全性、適法性、特定の目的への適合性を含む、事実上又は法律上の一切の不具合がないことにつき、明示的にも黙示的にも保証は行いません。なお、セキュリティ等への欠陥・エラー・バグがないことについても保証しません。
したがって、本プログラムの使用が原因で発生した健康被害や不利益、トラブルについては、山口達郎は一切の責任を負いません。

---
#### ライセンス

このExPReSSは、山口達郎によって作成されたものであり、 [クリエイティブ・コモンズ 表示 - 非営利 - 継承 4.0 国際 ライセンス](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ja)の下に提供されています。
This ExPReSS are created by Tatsuro Yamaguchi and licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
詳細はLICENSEファイルを参照してください。

##### CC BY-NC-SA 4.0（表示 - 非営利 - 継承 4.0 国際）

あなたは以下の条件に従う限り、自由に：
- 共有 — どのようなメディアやフォーマットでも資料を複製したり、再配布できます。
- 翻案 — マテリアルをリミックスしたり、改変したり、別の作品のベースにしたりできます。
- あなたがライセンスの条件に従っている限り、許諾者がこれらの自由を取り消すことはできません。
- あなたの従うべき条件は以下の通りです。
- 表示 — あなたは適切なクレジットを表示し、ライセンスへのリンクを提供し、 変更があったらその旨を示さなければなりません。これらは合理的であればどのような方法で行っても構いませんが、許諾者があなたやあなたの利用行為を支持していると示唆するような方法は除きます。


ーーーーー クレジット ーーーーー
- Copyright (c) 2025 Tatsuro Yamaguchi
- このExPReSSは、山口達郎によって作成されたものであり、 クリエイティブ・コモンズ 表示 - 非営利 - 継承 4.0 国際 ライセンスの下に提供されています。
- This software, 'ExPReSS', are created by Tatsuro Yamaguchi and licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

ーーーーーーーーーーーーーーーー

- 非営利 — あなたは 営利目的 でこの資料を利用してはなりません。
- 掲載・転載・一部利用および企業アカウントでのSNSへの掲載は営利目的の範疇とみなします。また、企業が主催し集客するセミナーや講演での利用や配布も営利目的とみなします）
- 注意）企業内において自社の社員教育に利用することは可能である。
- 継承 — もしあなたがこの資料をリミックスしたり、改変したり、加工した場合には、あなたはあなたの貢献部分を元の作品と同じクレジット表示とライセンスの下に頒布しなければなりません。
- 追加的な制約は課せません — あなたは、このライセンスが他の者に許諾することを法的に制限するようないかなる法的規定も技術的手段も適用してはなりません。

注意：
- あなたは、マテリアルの中でパブリック・ドメインに属している部分に関して、あるいはあなたの利用が著作権法上の 例外や権利制限規定 にもとづく場合には、ライセンスの規定に従う必要はありません。
- 保証は提供されていません。ライセンスはあなたの利用に必要な全ての許諾を与えないかも知れません。例えば、 パブリシティ権、肖像権、人格権 などの他の諸権利はあなたがどのように資料を利用するかを制限することがあります。

＜必ずお読みください＞
- コモンズ証（わかりやすい著作権表示）：https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ja
- 現行の著作権法のもとで許諾内容を法的に担保するライセンス条項「利用許諾」（ライセンス原文）：https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.ja

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
