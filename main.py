# # https://youtu.be/A8ldqcFS5S8


from kivymd.app import MDApp
from kivy.lang.builder import Builder

from libs.yt_downloader import ScreenManaging


class YoutubeDownloaderApp(MDApp):
    def build(self):
        self.load_all_kv_files()
        return ScreenManaging()

    def load_all_kv_files(self):
        Builder.load_file('libs/yt_downloader.kv')
        Builder.load_file('screens/link_page.kv')
        Builder.load_file('screens/details_page.kv')
        Builder.load_file('screens/download_options.kv')
        Builder.load_file('screens/downloading_screen.kv')
        Builder.load_file('screens/loading.kv')
        Builder.load_file('components/qual_options.kv')


if __name__ == '__main__':
    YoutubeDownloaderApp().run()
