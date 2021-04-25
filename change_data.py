import pandas as pd
import numpy as np
import warnings
import sys

warnings.simplefilter("ignore")

#直近num件のデータを削除する関数
def delete_recent_data(df,num):
    data_size = len(df)
    delete_list = np.arange(data_size-num,data_size)
    df = df.drop(delete_list)
    return df

#特定のハンドサインを削除する関数
def delete_hand_sign(df,label_list,id):
    #指定されたidに対応する行を削除
    df = df[df[0]!=id]
    #削除した分,ハンドサインのidを詰める
    arr = np.array(df)
    index = np.where(arr[:,0]>id)[0]
    arr[index,0] = arr[index,0] - 1
    df = pd.DataFrame(arr)

    label_list = label_list.drop(id)  #idに対応する行を削除
    label_list = label_list.reset_index(drop=True)  #削除した分、ハンドサインのidを詰める
    return df,label_list

def add_hand_sign(label_list,name):
    size = len(label_list)
    dic = {0:name}
    label_list = label_list.append(dic,ignore_index=True)
    return label_list

data_path = "model/keypoint_classifier/keypoint.csv"
label_path = "model/keypoint_classifier/keypoint_classifier_label.csv"

#データの読み込み
df = pd.read_csv(data_path,header=None)
datasize = len(df)
label_list = pd.read_csv(label_path,header=None)

while True:
    try:
        print("終了するにはCtrl+Cを入力してください")
        #関数選択
        try:
            func_num = int(input("直近のデータを削除[1] 特定のハンドサインを削除[2] 新しいハンドサインを追加[3] 現在のデータを表示[4]:"))
            if func_num not in [1,2,3,4]:
                print("無効な値が入力されました\n")
                continue
        #func_numが数値ではないとき
        except ValueError:
            print("無効な値が入力されました\n")
            continue

        #func_num==1の時
        if func_num == 1:
            try:
                print(df)
                num = int(input("何件のデータを削除しますか？:"))
                #削除できるデータの件数かどうか
                if 0 < num < datasize:
                    df = delete_recent_data(df,num)
                    df.to_csv(data_path,header=False,index=False)
                else:
                    print("0より小さい、またはデータサイズ以上の値が入力されました\n")
                    continue
            #numが数値ではないとき
            except ValueError:
                print("無効な値が入力されました\n")
                continue

        #func_num==2の時
        if func_num == 2:
            try:
                print(label_list)
                id = int(input("削除したいクラスの番号を入力してください:"))
                if id in np.arange(len(label_list)):
                    df,label_list = delete_hand_sign(df,label_list,id)  #削除
                    #保存
                    df.to_csv(data_path,header=False,index=False)
                    label_list.to_csv(label_path,header=False,index=False)
                else:
                    print("無効な値が入力されました\n")
                    continue
            except ValueError:
                print("無効な値が入力されました\n")
                continue

        if func_num == 3:
            print(label_list)
            name = input("追加したいハンドサインの名前を入力してください:")
            label_list = add_hand_sign(label_list,name)
            label_list.to_csv(label_path,header=False,index=False)


        #func_num==3の時
        if func_num == 4:
            print("\nハンドサイン")
            print(label_list)
            print("\nデータ")
            print(df,"\n")

    #Ctrl+C入力時
    except KeyboardInterrupt:
        sys.exit("\n\nプログラムを終了します\n")
