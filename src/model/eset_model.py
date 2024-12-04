from .download_service import DownloadService
from .usb_service import USBService
from .server_service import ServerService


class ESETModel:
    def __init__(self):
        self.download_service = DownloadService()
        self.usb_service = USBService()
        self.server_service = ServerService()

    def download_file(self):
        """ダウンロード処理の実行"""
        success, message = self.download_service.download_file()
        return success, message

    def move_to_usb(self):
        """USBへの移動処理の実行"""
        success, message = self.usb_service.move_zip_to_usb()
        return success, message

    def move_to_server(self):
        """サーバーへの移動処理の実行"""
        success, message = self.server_service.move_zip_to_server()
        return success, message
