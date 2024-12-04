import os
from ctypes import windll
import glob
import shutil


class ServerService:
    def __init__(self):
        self.script_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

    def get_usb_drive(self):
        """
        USBドライブを取得する

        Returns:
            str: USBドライブのドライブレター
        """
        # 全てのドライブレターを取得
        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for i in range(26):
            if bitmask & (1 << i):
                drives.append(chr(65 + i) + ":\\")

        # USBドライブを検出
        usb_drive = None
        for drive in drives:
            if windll.kernel32.GetDriveTypeW(drive) == 2:  # 2はリムーバブルドライブ
                usb_drive = drive
                break

        return usb_drive

    def set_usb_path(self):
        """
        USBの対象フォルダのパスを取得する

        Returns:
            str: USBの対象フォルダのパス
        """
        usb_drive = self.get_usb_drive()
        if usb_drive is None:
            return False, "USBドライブが見つかりません。"

        # USBの対象フォルダのパスを設定
        usb_path = os.path.join(usb_drive, "三光システム", "ESET検出エンジン")

        # USBの対象フォルダの存在確認
        if os.path.exists(usb_path):
            return usb_path
        else:
            return False, "USBの対象フォルダが見つかりません。"

    def get_server_path(self):
        """
        サーバーの対象フォルダのパスを取得する

        Returns:
            str: サーバーの対象フォルダのパス
        """
        # サーバーの対象フォルダのパスを設定
        server_path = "Z:\\"

        # サーバーの対象フォルダの存在確認
        if os.path.exists(server_path):
            return server_path
        else:
            return False, "サーバーの対象フォルダが見つかりません。"

    def get_latest_zip_file(self):
        """
        最新のZIPファイルを取得する

        Returns:
            str: 最新のZIPファイルのパス
        """
        # USBフォルダ内のZIPファイルを検索し、最新のファイルを取得
        usb_path = self.set_usb_path()
        latest_zip_file = glob.glob(os.path.join(usb_path, "essupd*.zip"))
        if not latest_zip_file:
            return False, "ZIPファイルが見つかりません。"

        latest_zip_file = max(latest_zip_file, key=os.path.getctime)
        return latest_zip_file

    def remove_all_files(self, path):
        """
        サーバーの対象フォルダ内の"essupd*.zip"に一致するファイルを削除する

        Args:
            usb_path (str): サーバーの対象フォルダのパス
        Returns:
            tuple: (bool, str) 成功したかどうかとメッセージ
        """
        try:
            # "essupd*.zip"に一致するファイルを検索
            zip_files = glob.glob(os.path.join(path, "essupd*.zip"))
            for file_path in zip_files:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            return True, "指定されたZIPファイルの削除が完了しました。"
        except Exception as e:
            return (
                False,
                f"ZIPファイル削除中にエラーが発生しました: {str(e)}",
            )

    def move_zip_to_server(self):
        try:
            # USBの対象フォルダのパスを取得
            usb_path_result = self.set_usb_path()
            if isinstance(usb_path_result, tuple):
                return False, usb_path_result[1]
            usb_path = usb_path_result

            # 最新のZIPファイルを取得
            latest_zip_result = self.get_latest_zip_file()
            if isinstance(latest_zip_result, tuple):
                return False, latest_zip_result[1]
            latest_zip_file = latest_zip_result

            # サーバーの対象フォルダのパスを設定
            server_path_result = self.get_server_path()
            if isinstance(server_path_result, tuple):
                return False, server_path_result[1]
            server_path = server_path_result

            # サーバーの対象フォルダ内の全てのファイル/フォルダを削除
            remove_result = self.remove_all_files(server_path)
            if not remove_result[0]:
                return False, remove_result[1]

            # ZIPファイルをサーバーの対象フォルダに移動
            shutil.move(latest_zip_file, server_path)

            return True, "ZIPファイルの移動が完了しました。"

        except Exception as e:
            return False, f"エラーが発生しました: {str(e)}"
