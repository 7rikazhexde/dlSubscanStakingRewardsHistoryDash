import os
from tkinter import Tk, filedialog

import pandas as pd

# ユーザーにフォルダを指定してもらう
root = Tk()
root.withdraw()  # GUIを表示しない
folder_path = filedialog.askdirectory()  # フォルダ選択ダイアログを表示

# フォルダ内のcsvファイルのリストを取得
csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

# 各csvファイルを読み込み、一つのデータフレームに結合
df = pd.concat([pd.read_csv(os.path.join(folder_path, f)) for f in csv_files])

# Timestampカラムを基準に昇順でソート
df = df.sort_values("Timestamp")

# 結果をData.csvとして保存
df.to_csv(os.path.join(folder_path, "Data.csv"), index=False)
