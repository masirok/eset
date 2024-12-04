from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
from pathlib import Path
from dotenv import load_dotenv


class DownloadService:
    def __init__(self):
        load_dotenv()  # .envファイルから環境変数を読み込む
        self.serial_number = os.environ.get("ESET_SERIAL_NUMBER")
        self.password = os.environ.get("ESET_PASSWORD")
        if not self.serial_number or not self.password:
            raise ValueError(
                "環境変数 ESET_SERIAL_NUMBER または ESET_PASSWORD が設定されていません"
            )
        self.driver = None

    def setup_driver(self):
        """Chromeブラウザを起動し、指定されたURLにアクセスする。"""
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get("https://canon-its.jp/product/eset/users/index.html")

    def login_to_eset(self):
        """ESETのログインページに移動し、シリアル番号とパスワードを入力してログインする。"""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//input[@value='　ログインページに移動　']")
                )
            ).click()
            self.driver.switch_to.window(self.driver.window_handles[-1])

            # シリアル番号を入力
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "txtSerial"))
            ).send_keys(self.serial_number)

            # パスワードを入力
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "txtUser"))
            ).send_keys(self.password)

            # 利用規約に同意してログイン
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "chkAgree"))
            ).click()
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@value='　ログイン　']"))
            ).click()
            return True
        except Exception as e:
            print(f"ログイン中にエラーが発生: {e}")
            return False

    def download_detection_engine(self):
        """検出エンジンのダウンロードページに移動し、ダウンロードを開始する"""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@name, 'no4')]//p"))
            ).click()

            eset_download_url = (
                WebDriverWait(self.driver, 10)
                .until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//a[contains(@href, 'update_file.cgi')][@class='buttonDownload solid radius']",
                        )
                    )
                )
                .get_attribute("href")
            )
            self.driver.get(eset_download_url)

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "v11"))
            ).click()
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//input[@type='button'][contains(@onclick, '/v11/')][contains(@value, '最新')]",
                    )
                )
            ).click()
            return True
        except Exception as e:
            print(f"ダウンロード中にエラーが発生: {e}")
            return False

    def wait_for_download(self, downloads_path, timeout=600):
        """ダウンロードの完了を待機する"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                zip_files = [
                    f
                    for f in os.listdir(downloads_path)
                    if f.endswith(".zip") and f.startswith("essupd")
                ]
                temp_files = [
                    f
                    for f in os.listdir(downloads_path)
                    if f.endswith(".crdownload") or f.endswith(".tmp")
                ]

                if zip_files and not temp_files:
                    return True
                time.sleep(2)
            except Exception as e:
                print(f"ファイル検索中にエラーが発生: {e}")
                time.sleep(2)
        return False

    def download_file(self):
        """ダウンロードプロセス全体を実行する"""
        try:
            downloads_path = str(Path.home() / "Downloads")
            self.setup_driver()

            if not self.login_to_eset():
                raise Exception("ログインに失敗しました")

            if not self.download_detection_engine():
                raise Exception("ダウンロード開始に失敗しました")

            if not self.wait_for_download(downloads_path):
                raise Exception("ダウンロードがタイムアウトしました")

            return True, "ダウンロードが完了しました"

        except Exception as e:
            return False, str(e)
        finally:
            if self.driver:
                self.driver.quit()
