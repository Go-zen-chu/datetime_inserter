# datetime_inserter

写真の EXIF 情報から時間を抜き出して、ファイル名にinsertするスクリプト。EXIF.py を利用させてもらっています。

## Usage 

```
python datetime_inserter.py directoryPath fileName
```

```
python datetime_inserter.py ~/Desktop/myphotos MyJourney
```
これで、 myphotos 内の画像ファイルに MyJourney_時間.jpg のような名前を付けます。
