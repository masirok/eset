import os
from ctypes import windll
import glob
import shutil


class USBService:
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

    def get_latest_zip_file(self):
        """
        最新のZIPファイルを取得する

        Returns:
            str: 最新のZIPファイルのパス
        """
        # ダウンロードフォルダのパスを設定
        download_path = os.path.join(os.environ["USERPROFILE"], "Downloads")

        # ZIPファイルを検索し、最新のファイルを取得
        latest_zip_file = glob.glob(os.path.join(download_path, "essupd*.zip"))
        if not latest_zip_file:
            return False, "ZIPファイルが見つかりません。"

        latest_zip_file = max(latest_zip_file, key=os.path.getctime)
        return latest_zip_file

    def remove_all_files(self, path):
        """
        USBの対象フォルダ内の全てのファイル/フォルダを削除する

        Args:
            usb_path (str): USBの対象フォルダのパス
        Returns:
            tuple: (bool, str) 成功したかどうかとメッセージ
        """
        try:
            for file_name in os.listdir(path):
                file_path = os.path.join(path, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                else:
                    shutil.rmtree(file_path)
            return True, "フォルダ内のファイル/フォルダの削除が完了しました。"
        except Exception as e:
            return (
                False,
                f"フォルダ内のファイル/フォルダ削除中にエラーが発生しました: {str(e)}",
            )

    def move_zip_to_usb(self):
        """
        最新のZIPファイルをUSBに移動する

        Returns:
            tuple: (bool, str) 成功したかどうかとメッセージ
        """
        try:
            # USBの対象フォルダのパスを取得
            usb_path = self.set_usb_path()
            if not usb_path[0]:
                return False, usb_path[1]

            # 最新のZIPファイルを取得
            latest_zip_file = self.get_latest_zip_file()
            if not latest_zip_file[0]:
                return False, latest_zip_file[1]

            # USBの対象フォルダ内の全てのファイル/フォルダを削除
            success, message = self.remove_all_files(usb_path)
            if not success:
                return False, message

            # ZIPファイルをUSBに移動
            shutil.move(latest_zip_file, usb_path)

            return True, "ファイルの移動が完了しました。"

        except Exception as e:
            return False, f"エラーが発生しました: {str(e)}"
