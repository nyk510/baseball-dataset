# Baseball Dataset

日本プロ野球のデータを取得するモジュール `npbdata` を管理するリポジトリです.

## Requirements

```txt
joblib==0.11
jupyter==1.0.0
lxml==4.2.1
matplotlib==2.1.0
notebook==5.2.1
numpy==1.14.2
pandas==0.21.0
python-dotenv==0.8.2
tqdm==4.19.4
```

## Prepare

```bash
docker build -t npb .
docker run -it --name npb-data -p 7000:8888 -v ${PWD}:/npb npb
```

## Usage

### 打者のデータの取得

```bash
python fetch_hitters.py
```

実行すると, 2008 年から 2017 年までの規定打席に到達した打者の打撃結果を取得し `./data/hitters/{year}` 配下に tsv ファイルとして保存します.

```txt
./
├── Dockerfile
├── data
│   └── hitters
│       ├── 2012
│       │   ├── サブロー.tsv
│       │   ├── バルディリス.tsv
│       │   ├── フェルナンデス.tsv
│       │   ├── ヘルマン.tsv
│       │   ├── ペーニャ.tsv
│       │   ├── マートン.tsv
│       │   ├── ミレッジ.tsv
│       │   ├── ラミレス.tsv
│       │   ├── 阿部慎之助.tsv
│       │   ├── 井口資仁.tsv
│       │   ├── 井端弘和.tsv
│       │   ├── 稲葉篤紀.tsv
│       │   ├── 岡田幸文.tsv
│       │   ├── 角中勝也.tsv
│       │   ├── 銀次.tsv
│       │   ├── 栗山巧.tsv
│       │   ├── 後藤光尊.tsv
│       │   ├── 荒波翔.tsv
│       │   ├── 荒木雅博.tsv
│       │   ├── 今江敏晃.tsv
│       │   ├── 根元俊一.tsv
│       │   ├── 坂本勇人.tsv
│       │   ├── 糸井嘉男.tsv
│       │   ├── 秋山翔吾.tsv
```

### 試合結果の取得

```bash
python main.py
```