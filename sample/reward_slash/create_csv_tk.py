import os
from tkinter import Tk, filedialog

import pandas as pd

# ユーザーにフォルダを指定してもらう
root = Tk()
root.withdraw()  # GUIを表示しない
folder_path = filedialog.askdirectory()  # フォルダ選択ダイアログを表示

# フォルダパスを出力して確認
print(f"指定されたフォルダパス: {folder_path}")

# フォルダ内のcsvファイルのリストを取得
csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

# CSVファイルリストを出力して確認
print(f"CSVファイルリスト: {csv_files}")

# CSVファイルが見つからない場合の処理
if not csv_files:
    print("指定されたフォルダにはCSVファイルが含まれていません。")
else:
    # 各csvファイルを読み込み、一つのデータフレームに結合
    df = pd.concat([pd.read_csv(os.path.join(folder_path, f)) for f in csv_files])

    # Timestampカラムを基準に昇順でソート
    df = df.sort_values("Timestamp")

    # 結果をData.csvとして保存
    df.to_csv(os.path.join(folder_path, "Data.csv"), index=False)
    print("Data.csvとして保存されました。")
