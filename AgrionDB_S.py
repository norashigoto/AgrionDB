#################################################################
#                                       Create on 2023/07/11    #
#   InVoiceNo Search System (Sub)                               #
#       1.0     : GetInBoxFile                                  #
#                                                               #
#################################################################
import AgrionDB_def  as S_Def
import dash  
#from dash_extensions import Download
#import dash_core_components as dcc
#import dash_html_components as html
from dash import Dash
from dash import Dash, html, dcc, dash_table
import json
import os
import  io, base64
import pandas               as pd
from datetime   import datetime
import numpy    as np


# 2.0 WebDesign定義
def SetWebLayout():
    # AgrionDB読込ボタン
    F_Inp_Btns = html.Button("ファイル指定", id='Inp_btn', n_clicks=0)
    F_Inp_Btn   = dcc.Upload(id='agfile_btn',children=F_Inp_Btns, multiple=True)

    # 栽培日誌ダウンロードボタン
    F_Note_Btns  = html.Button("栽培日誌作成",id="note_btn", n_clicks=0)
    F_Note_Btn   = dcc.Download(id="note_dwn")

    # Layout定義
    Area_Ctl    = html.Div(html.Div([F_Inp_Btn,F_Note_Btn,F_Note_Btns]))

    return Area_Ctl


# 3.0 Agrionファイル内容読込み
def AgrionDB_Read(InXName,content):
    # 1.1 割付工数ファイル読込
    decoded         = None
    if content:
        _, content_string   = content.split(',')
        decoded             = base64.b64decode(content_string)        
        try :
            df_raw          = pd.read_excel(io.BytesIO(decoded),header=None)

            header_row_idx  = df_raw[df_raw.iloc[:, 1].astype(str).str.contains('行番号', na=False)].index[0]

            # ヘッダー行とその下を抽出、A列は除去
            df_out = df_raw.iloc[header_row_idx:]
            df_out.columns = df_out.iloc[0]  # 最初の行をカラム名に
            df_out = df_out.drop(df_out.index[0])  # ヘッダー行を削除
            df_out = df_out.drop(df_out.columns[0], axis=1)  # A列を削除

            Flg     = True



        except Exception as e:
            print(" ・ファイル読込エラー : ",InXName)
            df_out  = pd.DataFrame()
            Flg     = False

    return df_out,Flg

# 4.0 栽培日誌作成
def AgrionDialy_Create(df):
    # 圃場リスト作成
    df_tmp  = df.loc[df["作業名"]=="開始","場所名"].drop_duplicates()
    HojoName = df_tmp.tolist()

    # 対象圃場データ出力
    df_ad = df[(df["場所名"].isin(HojoName)) & (df["作物名"]=="ねぎ")].sort_values(by="場所名").reset_index(drop=True)  # 対象DB抽出
    df_out  = AgrionDialy_NewDB_Create(HojoName)    # 栽培日誌初期DB作成
    df_out  = AgrionDialy_Teishoku(df_ad,df_out)    # 情報追加　”定植”
    df_out  = AgrionDialy_Tuchiyose(df_ad,df_out)   # 情報追加　”土寄”
    df_out  = AgrionDialy_553(df_ad,df_out)         # 情報追加　”防草”
    df_out  = AgrionDialy_Josou(df_ad,df_out)       # 情報追加　”除草（非選択）”
    df_out  = AgrionDialy_Naburoro(df_ad,df_out)    # 情報追加　”除草（選択）”
    df_out  = AgrionDialy_YakuAmi(df_ad,df_out)     # 情報追加　”防除（アミスター）”
    df_out  = AgrionDialy_YakuPre(df_ad,df_out)     # 情報追加　”除草（プレオ）”
    print(df_out)

    return df_out

# 4.1 栽培日誌空DB作成
def AgrionDialy_NewDB_Create(TN_lst):
    df_out = pd.DataFrame({"場所名":TN_lst})
    df_out  = df_out.reindex(columns=["場所名","定植","土寄","５５３","グリホ","ナブロロ","アミスタ","プレオ"])
    return df_out

# 4.2 定植DB構築
def AgrionDialy_Teishoku(df_in, df_out):
    for HN in df_in["場所名"].drop_duplicates().tolist():
        TNinfo_lst  = df_in[(df_in["場所名"] == HN) & (df_in["作業名"].str.contains("定植", na=False))]["開始日時"].tolist()
        df_out.loc[df_out["場所名"]==HN,"定植"] = TNinfo_lst[0].strftime("%m/%d") if TNinfo_lst else np.nan

    return df_out

# 4.3 土寄DB構築
def AgrionDialy_Tuchiyose(df_in, df_out):
    for HN in df_in["場所名"].drop_duplicates().tolist():
        TNinfo_lst  = df_in[(df_in["場所名"] == HN) & (df_in["作業名"].str.contains("土寄", na=False))]["開始日時"].tolist()
        if TNinfo_lst:
            TNinfo_tmp  = max(TNinfo_lst)
            TNinfo      = "[" + str(len(TNinfo_lst)) + "] " + TNinfo_tmp.strftime("%m/%d")
        else:
            TNinfo  = ""
        df_out.loc[df_out["場所名"]==HN,"土寄"] = TNinfo


    return df_out

# 4.4 防草DB構築
def AgrionDialy_553(df_in, df_out):
    for HN in df_in["場所名"].drop_duplicates().tolist():
        TNinfo_lst  = df_in[(df_in["場所名"] == HN) & (df_in["作業名"].str.contains("防草", na=False))]["開始日時"].tolist()
        if TNinfo_lst:
            TNinfo_tmp  = max(TNinfo_lst)
            TNinfo      = "[" + str(len(TNinfo_lst)) + "] " + TNinfo_tmp.strftime("%m/%d")
        else:
            TNinfo  = ""
        df_out.loc[df_out["場所名"]==HN,"５５３"] = TNinfo


    return df_out

# 4.5 除草（非選択）DB構築
def AgrionDialy_Josou(df_in, df_out):
    for HN in df_in["場所名"].drop_duplicates().tolist():
        TNinfo_lst  = df_in[(df_in["場所名"] == HN) & (df_in["作業名"].str.contains("非選択", na=False))]["開始日時"].tolist()
        if TNinfo_lst:
            TNinfo_tmp  = max(TNinfo_lst)
            TNinfo      = "[" + str(len(TNinfo_lst)) + "] " + TNinfo_tmp.strftime("%m/%d")
        else:
            TNinfo  = ""
        df_out.loc[df_out["場所名"]==HN,"グリホ"] = TNinfo
    return df_out

# 4.6 除草（選択）DB構築
def AgrionDialy_Naburoro(df_in, df_out):
    for HN in df_in["場所名"].drop_duplicates().tolist():
        TNinfo_lst  = df_in[(df_in["場所名"] == HN) & (df_in["作業名"].str.contains("-選択-", na=False))]["開始日時"].tolist()
        if TNinfo_lst:
            TNinfo_tmp  = max(TNinfo_lst)
            TNinfo      = "[" + str(len(TNinfo_lst)) + "] " + TNinfo_tmp.strftime("%m/%d")
        else:
            TNinfo  = ""
        df_out.loc[df_out["場所名"]==HN,"ナブロロ"] = TNinfo
    return df_out

# 4.7 防除（アミスター）DB構築
def AgrionDialy_YakuAmi(df_in, df_out):
    for HN in df_in["場所名"].drop_duplicates().tolist():
        TNinfo_lst  = df_in[(df_in["場所名"] == HN) & (df_in["農薬名"].str.contains("アミスタ", na=False))]["開始日時"].tolist()
        if TNinfo_lst:
            TNinfo_tmp  = max(TNinfo_lst)
            TNinfo      = "[" + str(len(TNinfo_lst)) + "] " + TNinfo_tmp.strftime("%m/%d")
        else:
            TNinfo  = ""
        df_out.loc[df_out["場所名"]==HN,"アミスタ"] = TNinfo
    return df_out

# 4.7 防除（プレオ）DB構築
def AgrionDialy_YakuPre(df_in, df_out):
    for HN in df_in["場所名"].drop_duplicates().tolist():
        TNinfo_lst  = df_in[(df_in["場所名"] == HN) & (df_in["農薬名"].str.contains("プレオ", na=False))]["開始日時"].tolist()
        if TNinfo_lst:
            TNinfo_tmp  = max(TNinfo_lst)
            TNinfo      = "[" + str(len(TNinfo_lst)) + "] " + TNinfo_tmp.strftime("%m/%d")
        else:
            TNinfo  = ""
        df_out.loc[df_out["場所名"]==HN,"プレオ"] = TNinfo
    return df_out





# DataFrameをExcelファイルに変換し、バイトで返す関数
def to_excel_bytes_io(df,df_ad):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='data')
        df_ad.to_excel(writer, index=False, sheet_name='栽培日誌')

    output.seek(0)
    return output.read()

# DataFrameをマージ
def df_marge(df_1, df_2):
    df_tmp  = df_1
    df_out  = pd.merge(df_tmp,df_2,on="活動記録ID",how="outer",suffixes=('','_del'))

    for df_col in df_out.columns:
        if "_del" in df_col:
            df_out = df_out.drop(columns=df_col)

    return df_out