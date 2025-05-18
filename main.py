#################################################################
#                                       Create on 2025/05/02    #
#   AgrionDB Create                                             #
#                                                               #
#################################################################
import  io, base64
import openpyxl
import dash  
from dash import Dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

#from dash_extensions.snippets import send_bytes

import pandas   as pd
import webbrowser
import AgrionDB_def  as S_Def
import AgrionDB_S as S_S

####################
# 1.0 初期設定
####################
SD = S_Def.def_val()
df_all = pd.DataFrame()


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

####################
# 3.0 Dash環境設定
####################
app             = dash.Dash(__name__,update_title='しばらくお待ちください')           # App定義
app.layout      = SetWebLayout()            # Layout定義
server          = app.server



if __name__ == '__main__':
    print("------------------------------------------------")
    print("- AgrionDB Create (" , SD.VerNo ,")-")
    print("------------------------------------------------")
    #webbrowser.open("http://127.0.0.1:8051/")
    #app.run(debug=False,port=8051)
    app.run(debug=False)

