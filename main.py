import  io, base64
import openpyxl
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas   as pd

import AgrionDB_def  as S_Def
import AgrionDB_S as S_S

####################
# 1.0 初期設定
####################
SD = S_Def.def_val()
df_all = pd.DataFrame()



####################
# 3.0 Dash環境設定
####################
app             = dash.Dash(__name__,update_title='しばらくお待ちください')           # App定義
app.layout      = S_S.SetWebLayout()            # Layout定義
server          = app.server

########################################################################
# 4.    コールバック準備
########################################################################
# 4.1   AgrionDB読込
@app.callback(  Output('agfile_btn','style'),
                Input('agfile_btn', 'filename'), Input('agfile_btn', 'contents'),
                prevent_initial_call=True )
def UploadBtn(InXlsName,contents):
    # 0. 初期設定
    global      df_all
    work_flg    = False
    sehi_flg    = False
    yaku_flg    = False
    kiki_flg    = False
    memb_flg    = False

    # 1. ArigionDB読込
    for content_tmp,InXName in zip(contents,InXlsName):
        # DB読込
        df_tmp, Flg = S_S.AgrionDB_Read(InXName,content_tmp)
        print(InXName,Flg)
        # DB種類判別
        if Flg == False: continue
        
        if   "作業実績"         in InXName:     
            df_work     = df_tmp
            work_flg    = True
        elif "施肥記録"         in InXName:     
            df_sehi     = df_tmp
            sehi_flg    = True
        elif "農薬使用記録"     in InXName:     
            df_yaku     = df_tmp
            yaku_flg    = True
        elif "機材使用実績"     in InXName:     
            df_kiki     = df_tmp
            kiki_flg    = True
        elif "メンバー活動実績" in InXName:     
            df_memb     = df_tmp
            memb_flg    = True
        else:           continue
    if work_flg == False:
        print("作業実績ファイルを指定してください")
        raise PreventUpdate

    # DB結合
    df_out      = df_work
    if sehi_flg == True :
        df_out  = S_S.df_marge(df_out,df_sehi)
    if yaku_flg == True :
        df_out  = S_S.df_marge(df_out,df_yaku)
    if kiki_flg == True :
        df_out  = S_S.df_marge(df_out,df_kiki)
    if memb_flg == True :
        df_out  = S_S.df_marge(df_out,df_memb)
    df_all = df_out

    return dash.no_update

# 4.2 栽培日誌ダウンロード
@app.callback(  Output('note_dwn','data'),
                Input('note_btn', 'n_clicks'),
                prevent_initial_call=True )
def UploadBtn(n_clicks):
    # 栽培日誌作成
    df_ad = S_S.AgrionDialy_Create(df_all)

    return dcc.send_bytes(lambda b: b.write(S_S.to_excel_bytes_io(df_all,df_ad)), "df_out.xlsx")




# ローカル実行用
if __name__ == "__main__":
    print("------------------------------------------------")
    print("- AgrionDB Create (" , SD.VerNo ,")-")
    print("------------------------------------------------")
    app.run(debug=True)
