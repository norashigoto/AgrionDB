import dash
from dash import html

# Dashアプリケーションの作成
app = dash.Dash(__name__)
server = app.server  # gunicornが利用するFlaskサーバ

# アプリのレイアウト定義
app.layout = html.Div([
    html.H1("Render + Dash アプリケーション"),
    html.P("これはRender上で動作するDashサンプルです。")
])

# ローカル実行用
if __name__ == "__main__":
    app.run(debug=True)
