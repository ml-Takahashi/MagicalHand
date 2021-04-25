import pyautogui
import sys
import time

XSIZE,YSIZE=1440,900  # 画面サイズ
STOP_RATE=0.4  # 手の面積が画面の何割を占めたらプログラムを終了するか
XMIN,XMAX,YMIN,YMAX = 300,900,300,500  # 画像上での座標.ここのmax値とmin値の幅を狭めるほど小さい指の動きでのマウス操作が可能になる.
SIDE_SCALE,VERTICAL_SCALE = XSIZE/(XMAX-XMIN),YSIZE/(YMAX-YMIN)  # 画像上の座標とpc上の座標の縮尺(体感値)
SCROLLSPEED = 3  # マウスのスクロールのスピード

# 指の動きをマウスの動きに置き換えるクラス
class Finger2Mouse:
    def __init__(self):
        pass
    # 画像内での座標をpc上の座標に置き換えるメソッド
    def calc_coordinate(self,coordinate):
        #下のkeyUp("command")はchoose_appのための処理.
        #choose_appか上下左右のスクロール以外のメソッドが
        #呼び出されたときにどのアプリを選択するか決定するため.
        pyautogui.keyUp("command")
        x = int(SIDE_SCALE*(coordinate[0]-XMIN))
        y = int(VERTICAL_SCALE*(coordinate[1]-YMIN))
        # 画面のサイズをはみ出した場合の処理
        if x >= XSIZE:
            x = XSIZE - 10
        elif x <= 0:
            x = 10
        if y >= YSIZE:
            y = YSIZE - 10
        elif y <= 0:
            y = 10
        return x,y

    # マウスを動かす(両手パー)
    def move_mouse(self,coordinate):
        x,y = self.calc_coordinate(coordinate)
        pyautogui.moveTo(x,y)  # マウス移動

    # 左クリック(右手１本指)
    def leftclick(self,coordinate):
        x,y = self.calc_coordinate(coordinate)
        pyautogui.click(x,y,clicks=1,button="left")  # 左クリック

    # 右クリック(右手２本指)
    def rightclick(self,coordinate):
        x,y = self.calc_coordinate(coordinate)
        pyautogui.click(x,y,clicks=1,button="right",duration=0.2)  #右クリック

    # ドラッグ(右手3本指)
    def drag(self,coordinate):
        x,y = self.calc_coordinate(coordinate)
        pyautogui.dragTo(x,y,button="left")  # ドラッグ

    # 上/右スクロール(左手1本指)
    def upper_right_scroll(self,all_coordinate,brect):
        if all_coordinate[8][0]==(brect[2]-1):
            pyautogui.hscroll(SCROLLSPEED)  # 右スクロール
        else:
            pyautogui.scroll(SCROLLSPEED)  # 右スクロール

    # 下/左スクロール(左手2本指)
    def under_left_scroll(self,all_coordinate,brect):
        if all_coordinate[12][0]==(brect[2]-1):
            pyautogui.hscroll(-SCROLLSPEED)  # 左スクロール
        else:
            pyautogui.scroll(-SCROLLSPEED)  # 下スクロール

    # アプリ選択(左手3本指)
    def choose_app(self):
        pyautogui.keyDown("command")
        pyautogui.keyDown("Tab")
        pyautogui.keyUp("Tab")

    # 音声認識(右親指)
    def voice_recognition(self):
        pyautogui.keyDown("fn")
        pyautogui.keyUp("fn")
        pyautogui.keyDown("fn")
        pyautogui.keyUp("fn")
        time.sleep(3)


    # プログラム停止判定(両手パー)
    def stop(self,brect):
        area = (brect[2]-brect[0])*(brect[3]-brect[1])
        if area > XSIZE*YSIZE*STOP_RATE:
            sys.exit()  # プログラム終了
