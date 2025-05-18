import dash
from dash import html, dcc

import AgrionDB_def  as S_Def

####################
# 1.0 初期設定
####################
SD = S_Def.def_val()


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


# Dashアプリケーションの作成
#app = dash.Dash(__name__)
#server = app.server  # gunicornが利用するFlaskサーバ

# アプリのレイアウト定義
#app.layout = html.Div([
#    html.H1("Render + Dash アプリケーション"),
#    html.P("これはRender上で動作するDashサンプルです。")
#])

# ローカル実行用
if __name__ == "__main__":
    print("------------------------------------------------")
    print("- AgrionDB Create (" , SD.VerNo ,")-")
    print("------------------------------------------------")
    app.run(debug=True)
