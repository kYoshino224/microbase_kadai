# microbaseプレインターン課題
- [概要](#概要)
- [関数の説明](#関数の説明)
- [工夫](#工夫)
- [今後の展望](#今後の展望)

## 概要
- ハンコ内の文字を読み取るプログラムです。
- ライブラリのバージョンはrequirements.txtを参照してください。
- azure のAPIを用いて文字を検出したあと、直線を検知します。直線群で区切られた領域それぞれの中にある文字で、語彙データベースと照らし合わせながらアナグラムを作ります。
- $ python main.py image_pathで実行できます。環境変数としてENDPOINT、VISION_KEYを、azure APIのendpoint, keyにそれぞれ登録してください。

## 関数の説明
### api.py
azureのAPIを用いて文字を抽出します。

input:画像のpath

output: pd.DataFrame(column=[“word”, “x”, “y”, ”gradient”, “region”])

### character_to_word.py
領域ごとに文字からアナグラムで単語を作ります。

input: pd.DataFrame(column=[“word”, “x”, “y”, ”gradient”, “region”])

output:[“abc”,…]

### concat_number.py
数字は検出された順で一つの単語とみなします。

input: pd.DataFrame(column=[“word”, “x”, “y”, ”gradient”, “region”])

output: pd.DataFrame(column=[“word”, “x”, “y”, ”gradient”, “region”])

### split_region.py
文字を直線で区分けされた領域で分類します。

input: (word_list=pd.DataFrame(column=[“word”, “x”, “y”, ”gradient”, “region”]), line_list=[[gradient,intercept],…])

output:pd.DataFrame(column=[“word”, “x”, “y”, ”gradient”, “region”])

## 工夫
- pyocrは全く検知してくれなかったので、急遽azureのAPIを使うことにしました。
- database/word_list.csvは、[語彙データベース](http://www17408ui.sakura.ne.jp/tatsum/database.html)と、地名リストを統合させたものです。
- 直線に跨って語句が存在することはほぼ無いので、直線を検知して区切ることで、アナグラムの際に総当たりの数が減って高速かつ正確に推定できました。
- 「海」と「運」でアナグラムができてしまったため、一文字ずつ傾きを計算し、その文字の水平線の延長線上にあるかどうかを判定する部分を追加しました。

## 今後の展望
- 一周に渡って文字が書かれているものなどは誤検知されてしまいます。
- 語彙リストをより充実させる必要があります。名前のリストなども追加すれば、検知漏れが少なくなると思われます。
- エッジとocrで検出漏れをダブルチェックするコードを書こうとしましたが、チェックしたところで再度画像認識させても文字は検出してくれないのではと思い、やめました。この部分がより発展できれば、より良いプログラムになると思います。「局」の部分がそもそも認識できていないのが1番の課題です。
