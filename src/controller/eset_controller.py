from ..view.eset_view import ESETView
from ..model.eset_model import ESETModel
import flet as ft


class ESETController:
    """ESETアプリケーションのコントローラークラス"""

    def __init__(self, view: ESETView, model: ESETModel):
        """
        コントローラーの初期化

        Args:
            view (ESETView): ビューインスタンス
            model (ESETModel): モデルインスタンス
        """
        self.view = view
        self.model = model

        # イベントハンドラを直接設定
        self.view.download_button.on_click = self.handle_download
        self.view.move_to_usb_button.on_click = self.handle_move_to_usb
        self.view.move_to_server_button.on_click = self.handle_move_to_server
        self.view.exit_button.on_click = self.handle_exit

    def handle_download(self, _):
        """
        ダウンロードボタンのクリックハンドラ

        Args:
            _: クリックイベント
        """
        try:
            self.view.status_text.visible = True
            self.view.update_status("ダウンロード中...")
            success, message = self.model.download_file()
            if success:
                self.view.download_button.style = ft.ButtonStyle(bgcolor=ft.colors.GREY)
                self.view.download_button.disabled = True
                self.view.download_button.text = "ダウンロード完了"
                self.view.status_text.value = "ダウンロードが完了しました"
                self.view.status_text.visible = False
                self.view.page.update()
            else:
                self.view.update_status(f"エラー: {message}")
        except Exception as ex:
            self.view.update_status(f"エラー: {str(ex)}")

    def handle_move_to_usb(self, _):
        """
        USBボタンのクリックハンドラ

        Args:
            _: クリックイベント
        """
        try:
            # モデルを使ってUSBへの移動処理を実行
            self.view.status_text.visible = True
            self.view.update_status("ZIPファイルをUSBへ移動中...")
            success, message = self.model.move_to_usb()
            if success:
                self.view.move_to_usb_button.style = ft.ButtonStyle(
                    bgcolor=ft.colors.GREY
                )
                self.view.move_to_usb_button.disabled = True
                self.view.move_to_usb_button.text = "USBへの移動完了"
                self.view.status_text.value = "USBへの移動が完了しました"
                self.view.status_text.visible = False
                self.view.update_status()
            else:
                self.view.update_status(f"エラー: {message}")
        except Exception as ex:
            self.view.update_status(f"エラー: {str(ex)}")

    def handle_move_to_server(self, _):
        """
        サーバーボタンのクリックハンドラ

        Args:
            _: クリックイベント
        """
        try:
            # モデルを使ってサーバーへの移動処理を実行
            self.view.status_text.visible = True
            self.view.update_status("ZIPファイルをサーバーへ移動中...")
            success, message = self.model.move_to_server()
            if success:
                self.view.move_to_server_button.style = ft.ButtonStyle(
                    bgcolor=ft.colors.GREY
                )
                self.view.move_to_server_button.disabled = True
                self.view.move_to_server_button.text = "サーバーへの移動完了"
                self.view.status_text.value = "サーバーへの移動が完了しました"
                self.view.status_text.visible = False
                self.view.update_status()
            else:
                self.view.update_status(f"エラー: {message}")
        except Exception as ex:
            self.view.update_status(f"エラー: {str(ex)}")

    def handle_exit(self, _):
        """
        終了ボタンのクリックハンドラ

        Args:
            _: クリックイベント
        """
        self.view.page.window_close()
