import flet as ft
import os
import sys


class ESETView:
    def __init__(self):
        # Fletのメインページ
        self.page: ft.Page = None

        # ロゴ画像
        self.logo_image: ft.Image = None

        # 検出エンジンダウンロードボタン
        self.download_button: ft.ElevatedButton = None

        # ZIPファイルをUSBにコピーするボタン
        self.move_to_usb_button: ft.ElevatedButton = None

        # ZIPファイルをサーバーにコピーするボタン
        self.move_to_server_button: ft.ElevatedButton = None

        # 状態表示テキスト
        self.status_text: ft.Text = None

        # アプリ終了ボタン
        self.exit_button: ft.ElevatedButton = None

    def initialize(self, page: ft.Page):
        """ページの初期化とUIコンポーネントの設定"""
        # 1.受け取ったページオブジェクトをインスタンス変数に保存
        self.page = page

        # 2.ウィンドウの基本設定
        self.setup_window_properties()

        # 3.UIコンポーネントの作成
        self.create_components()

        # 4.レイアウトの構成
        self.setup_layout()

    def setup_window_properties(self):
        """ウィンドウプロパティの設定"""
        # ウィンドウのタイトル
        self.page.title = "ESET 検出エンジン ダウンロード"

        # 水平方向の配置設定（中央寄せ）
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # 垂直方向の配置設定（中央寄せ）
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER

        # ウィンドウの背景色を白に設定
        self.page.bgcolor = ft.colors.WHITE

        # ウィンドウのサイズを設定（幅400px、高さ400px）
        self.page.window.width = 400
        self.page.window.height = 450

    def create_components(self):
        """UIコンポーネントの作成"""
        # ロゴ画像のパス設定
        if getattr(sys, "frozen", False):
            # 実行可能ファイルとして実行している場合
            image_path = os.path.join(
                sys._MEIPASS, "assets", "images", "ESET_logo01.png"
            )
        else:
            # 通常のPythonスクリプトとして実行している場合
            image_path = "assets/images/ESET_logo01.png"

        # ロゴ画像
        self.logo_image = ft.Image(src=image_path, width=200)

        # ダウンロードボタン
        self.download_button = ft.ElevatedButton(
            text="ESET検出エンジンファイル\nダウンロード開始",
            icon=ft.icons.DOWNLOAD,
            style=ft.ButtonStyle(bgcolor=ft.colors.ORANGE),
        )

        # ZIPファイルをUSBに移動するボタン
        self.move_to_usb_button = ft.ElevatedButton(
            text="ZIPファイルをUSBへ移動",
            icon=ft.icons.USB,
            style=ft.ButtonStyle(bgcolor=ft.colors.BLUE),
        )

        # ZIPファイルをサーバーに移動するボタン
        self.move_to_server_button = ft.ElevatedButton(
            text="ZIPファイルをサーバーへ移動",
            icon=ft.icons.UPLOAD,
            style=ft.ButtonStyle(bgcolor=ft.colors.GREEN),
        )

        # 状態表示テキスト
        self.status_text = ft.Text(value="", size=16)

        # アプリ終了ボタン
        self.exit_button = ft.ElevatedButton(
            text="終了",
            icon=ft.icons.EXIT_TO_APP,
            style=ft.ButtonStyle(bgcolor=ft.colors.RED),
        )

    def setup_layout(self):
        """レイアウトの構成"""
        self.page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Column(
                            controls=[
                                self.logo_image,
                                self.download_button,
                                self.move_to_usb_button,
                                self.move_to_server_button,
                                self.status_text,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                        ),
                        ft.Column(
                            controls=[self.exit_button],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=40,  # コンポーネント間のスペース
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )

    def update_status(self, message: str):
        """ステータスメッセージの更新"""
        self.status_text.value = message
        self.page.update()
