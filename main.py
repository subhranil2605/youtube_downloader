# from kivymd.app import MDApp
# from kivy.lang.builder import Builder
# from kivy.core.window import Window
# import asynckivy as ak
# from pytube import YouTube
#
#
# class YoutubeDownloaderApp(MDApp):
#     res_items = []
#     yt = None
#
#     def build(self):
#         Window.size = [320, 600]
#         return Builder.load_file('yt_downloader.kv')
#
#

#
#
#     def download_video(self):
#         url_text = self.root.ids.url
#
#         async def some_task():
#             # yt = await ak.run_in_thread(lambda: YouTube(url_text.text))
#             stream = await ak.run_in_thread(lambda: self.yt.streams.filter(
#                 progressive=True).get_by_resolution(f"{res}"))
#             await ak.run_in_thread(lambda: stream.download())
#             print('done')
#
#         ak.start(some_task())
#
#
# if __name__ == "__main__":
#     YoutubeDownloaderApp().run()
#
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
