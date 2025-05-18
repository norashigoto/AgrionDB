import dash
from dash import html

# Dashアプリケーションの作成
app_ds = dash.Dash(__name__)
server = app_ds.server  # gunicornが利用するFlaskサーバ

# アプリのレイアウト定義
app_ds.layout = html.Div([
    html.H1("Render + Dash アプリケーション"),
    html.P("これはRender上で動作するDashサンプルです。")
])

# ローカル実行用
if __name__ == "__main__":
    app_ds.run(debug=True)
