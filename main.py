import flet as ft
from src.view.eset_view import ESETView
from src.model.eset_model import ESETModel
from src.controller.eset_controller import ESETController


def main(page: ft.Page):
    # Viewの初期化
    view = ESETView()
    view.initialize(page)

    # Model, Controllerの初期化を追加
    model = ESETModel()
    controller = ESETController(view, model)


if __name__ == "__main__":
    ft.app(target=main)


# exe化するコマンド
# flet pack main.py --add-data "assets/images/*;assets/images" --add-data "src;src" --icon "assets/images/ESET_Logo02.ico" --name "ESET検出エンジンダウンロードアプリ"
# flet pack main.py --add-data "assets/images/*;assets/images" --add-data "src;src" --add-data ".env;." --icon "assets/images/ESET_Logo02.ico" --name "ESET検出エンジンダウンロードアプリ"
