from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivy.lang.builder import Builder
from kivy.core.window import Window
import asynckivy as ak
from pytube import YouTube


from kivymd.uix.menu import MDDropdownMenu


class YoutubeDownloaderApp(MDApp):

    res_items = []
    yt = None

    def build(self):
        Window.size = [320, 600]
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": i,
                "height": 40,
                "on_release": lambda x=i: self.set_item(x)
            } for i in self.res_items
        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )

        return Builder.load_file('yt_downloader.kv')

    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def get_details(self):

        url_text = self.root.ids.url
        title = self.root.ids.title
        img_url = self.root.ids.thumbnail

        async def some_task():
            self.yt = await ak.run_in_thread(lambda: YouTube(url_text.text))
            title.text = await ak.run_in_thread(lambda: f"Title: {self.yt.title}")
            img_url.source = await ak.run_in_thread(lambda: self.yt.thumbnail_url)
            self.res_items = await ak.run_in_thread(lambda: [
                i.resolution for i in self.yt.streams.filter(progressive=True)])
            await ak.run_in_thread(lambda: self.build())

        ak.start(some_task())

    def set_item(self, res):
        self.root.ids.drop_down.text = res
        self.menu.dismiss()

    def download_video(self):
        url_text = self.root.ids.url
        res = self.root.ids.drop_down.text

        async def some_task():
            # yt = await ak.run_in_thread(lambda: YouTube(url_text.text))
            stream = await ak.run_in_thread(lambda: self.yt.streams.filter(
                progressive=True).get_by_resolution(f"{res}"))
            print(stream)
            await ak.run_in_thread(lambda: stream.download())
            print('done')
        ak.start(some_task())


if __name__ == "__main__":
    YoutubeDownloaderApp().run()


# https://youtu.be/A8ldqcFS5S8
