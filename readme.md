# Baseball Dataset

## 説明
NPBのデータを取ってきて色々やりたーいのでデータセット作りました。

## データセットの説明

どういうデータが入ってるかざっくりと説明します。

### player_info_table.csv

選手の身長とか体重みたいな、個人的特徴ベクトル

+ team
+ 体重
+ 身長
+ 出身県（国）
+ 年俸

### pitcher(hitter)+年号.csv
その年の投手野手の公式記録。

+ 登板数
+ 勝利数

みたいな、ちょっと粒度の大きめのデータ

### match_up_table.csv

対戦記録。現在2009~2015までの全試合を格納.

* 場所
* Home Team
* Away Team
* Start Time
