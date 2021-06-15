from kivy.uix.screenmanager import ScreenManager
import asynckivy as ak
from pytube import YouTube

from components.qual_options import OptionListItem


class ScreenManaging(ScreenManager):
    yt = None
    res_items = []
    thm_url = ''
    title = ''

    def get_details(self, url):
        async def some_task():
            current_screen = self.current
            try:
                self.current = 'loading'
                self.yt = await ak.run_in_thread(lambda: YouTube(url))
                self.title = await ak.run_in_thread(lambda: f"Title: {self.yt.title}")
                self.thm_url = await ak.run_in_thread(lambda: self.yt.thumbnail_url)

                self.current = 'details'
                self.current_screen.ids.thumbnail.source = self.thm_url
                self.current_screen.ids.title.text = self.title

            except Exception as e:
                print(str(e))
                # if we get an error then come back to the main page
                self.current = current_screen

        ak.start(some_task())

    def get_download_options(self):
        async def some_task():
            current_screen = self.current
            try:
                self.current = 'loading'
                self.res_items = await ak.run_in_thread(
                    lambda: [i.resolution for i in self.yt.streams.filter(file_extension='mp4')])
                self.current = 'download_options'
                self.current_screen.ids.image.source = self.thm_url
                self.current_screen.ids.title.text = self.title
                self.res_items.pop()
                print(self.res_items)
                for i in self.res_items:
                    self.current_screen.ids.option_layout.add_widget(OptionListItem(
                        quality=i
                    ))

            except Exception as e:
                print(str(e))
                self.current = current_screen
        ak.start(some_task())

    def change_screen(self, scrn):
        self.current = scrn
