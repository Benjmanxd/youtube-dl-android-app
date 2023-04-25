from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.utils import platform
from datetime import datetime
from youtube_dl import YoutubeDL
import requests
import ssl
import re

if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.INTERNET])
ssl._create_default_https_context = ssl._create_unverified_context
DOWNLOAD_PATH = "/storage/emulated/0/Download"

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}

def safe_filename(s: str, max_length: int = 255) -> str:
    ntfs_characters = [chr(i) for i in range(0, 31)]
    characters = [ r'"', r"\#", r"\$", r"\%", r"'", r"\*",
                   r"\,", r"\.", r"\/", r"\:", r'"', r"\;",
                   r"\<", r"\>", r"\?", r"\\", r"\^", r"\|", 
                   r"\~", r"\\\\", ]
    pattern = "|".join(ntfs_characters + characters)
    regex = re.compile(pattern, re.UNICODE)
    filename = regex.sub("", s)
    return filename[:max_length].rsplit(" ", 0)[0]

class Root(BoxLayout):
    user_input = ObjectProperty(None)
    log_text = ObjectProperty(None)

    def __init__(self):
        super(Root, self).__init__()
        self.log("App is running")

    def clear_text(self):
        self.user_input.text = ""
        self.log_text.text = ""

    #def on_progress(self, stream, _, remains):
    #    total = stream.filesize
    #    percent = (total-remains) / total * 100
    #    self.log(f"Downloading at {percent:05.2f}", True)

    def download_audio(self, url):
        try:
            info_dict = None
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                title = safe_filename(info_dict.get('title', None)).replace(" ", "") if info_dict is not None else ""
                self.log("Start downloading mp3: %s" % title)
                ydl.download(url)
                self.log("Finish downloading mp3 %s at %s" % (title, DOWNLOAD_PATH))
            return True
        except Exception as ex:
            self.log("Caught exception: %s" % str(ex))
            self.log("Mp3 unavailable: %s" % url)
            return False

    def check_internet(self, url='http://www.google.com/', timeout=3):
        try:
            requests.head(url, timeout=timeout)
            self.log("Internet connection establlished")
            return True
        except requests.ConnectionError as ex:
            self.log(str(ex))
            self.log("Internet can't be established, please check wifi or mobile data")
            return False

    def log(self, download_text, same_line=False):
        now = datetime.now().isoformat(sep=" ", timespec="seconds")
        if not same_line:
            self.log_text.text += ("%s    %s\n" % (now, download_text))
        else:
            self.log_text.text += ("%s    %s\r" % (now, download_text))

    def audio_update(self):
        if not self.check_internet():
            return
        urls = self.user_input.text.split('\n')
        for url in urls:
            if url == "":
                continue
            self.log("Start processing url: %s" % url)
            self.download_audio(url)

class YoutubeDownloader(App):
    def build(self):
        return Root()

youtube_dl = YoutubeDownloader()
youtube_dl.run()
