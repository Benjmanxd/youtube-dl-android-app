import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class Root(BoxLayout):
    
    def __init__(self):
        super(Root, self).__init__()
    
    def download_files(self):
        print("downloading")

    def update_download_text(self):
        self.download_label.text = "hihi";

    def update(self):
        self.update_download_text()
        print("updated")


class YoutubeDownloader(App):
    def build(self):
        return Root()

youtube_dl = YoutubeDownloader()
youtube_dl.run()

