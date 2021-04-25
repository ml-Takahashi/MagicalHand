# Magical Hand
1.MediaPipe(Python版)を用いて手の姿勢推定を行い、検出したキーポイントを用いて、
簡易なMLPでハンドサインを認識します。pyautoguiを用いることでそのハンドサインに応じて左右クリック、
上下左右スクロール、アプリ選択などのGUI操作を可能にしました。

2.pyautoguiを用いることで、検出したキーポイントの座標とマウスの動きを対応させ、
手の動きに合わせたマウスの操作を可能にしました。

3.短時間でハンドサインの追加、削除、学習ができる。

# DEMO
デモの実行方法は以下です。
```bash
python main.py
```

デモ実行時には、以下のオプションが指定可能です。
* --device<br>カメラデバイス番号の指定 (デフォルト：0)
* --width<br>カメラキャプチャ時の横幅 (デフォルト：960)
* --height<br>カメラキャプチャ時の縦幅 (デフォルト：540)

### main.py
Magical Hand実行用のファイルです。<br>
ハンドサインに対応してpcが動きます。

### add_hand_sign.py
ハンドサイン認識用の学習データを記録することができます。

### change_data.py
記録されたハンドサインを選択的に削除できます。<br>
また、新しいハンドサインの名前を追加することもできます。

### train_model.py
ハンドサイン認識のモデル訓練用ファイルです。

### Operation
pc操作に関するファイルを格納するプログラムです。<br>
finger2mouse.pyの中にあるFinger2Mouseクラスのメソッドによってpcの操作を決めています。<br>
ここを変更すると操作方法も変更できます。

### model/keypoint_classifier
ハンドサイン認識に関わるファイルを格納するディレクトリです。<br>
以下のファイルが格納されます。
* 学習用データ(keypoint.csv)
* 学習済モデル(keypoint_classifier.tflite)
* ラベルデータ(keypoint_classifier_label.csv)

### utils/cvfpscalc.py
FPS計測用のモジュールです。

# Training
ハンドサイン認識、フィンガージェスチャー認識は、<br>学習データの追加、変更、モデルの再トレーニングが出来ます。

### ハンドサイン認識トレーニング方法
#### 1.学習データ収集
「k」を押すと、キーポイントの保存するモードになります（「MODE:Logging Key Point」と表示される）<br>
<img src="https://user-images.githubusercontent.com/37477845/102235423-aa6cb680-3f35-11eb-8ebd-5d823e211447.jpg" width="60%"><br><br>
「0」～「9」を押すと「model/keypoint_classifier/keypoint.csv」に以下のようにキーポイントが追記されます。<br>
1列目：押下した数字(クラスIDとして使用)、2列目以降：キーポイント座標<br>
<img src="https://user-images.githubusercontent.com/37477845/102345725-28d26280-3fe1-11eb-9eeb-8c938e3f625b.png" width="80%"><br><br>
キーポイント座標は以下の前処理を④まで実施したものを保存します。<br>
<img src="https://user-images.githubusercontent.com/37477845/102242918-ed328c80-3f3d-11eb-907c-61ba05678d54.png" width="80%">
<img
src="https://user-images.githubusercontent.com/37477845/102244114-418a3c00-3f3f-11eb-8eef-f658e5aa2d0d.png" width="80%"><br><br>

#### 2.モデル訓練
「[train_model.py](train_model.py)」を実行してください。

#### 3.学習データ、ハンドサイン削除、追加
「[change_data.py](change_data.py)」を実行してください。

# Requirement
- Python 3.8.x
- mediapipe 0.8.1
- OpenCV 3.4.2 or Later
- tensorflow 2.3.0 or Later

# Installation
- pip install pyautogui

# Author
高橋哉人
