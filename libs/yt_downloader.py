from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.label import MDLabel
from kivymd.toast import toast
import asynckivy as ak
from pytube import YouTube


from components.qual_options import OptionListItem


def byte_to_mb(b):
    return round(b / 10**6)


class ScreenManaging(ScreenManager):
    yt = None
    video_with_audio = []
    video_without_audio = []
    audio_files = []
    thm_url = ''
    title = ''
    itag = 0
    res = ''
    previous_progress = 0
    liveprogress = 0

    def get_details(self, url):
        async def some_task():
            current_screen = self.current
            try:
                self.current = 'loading'
                self.yt = await ak.run_in_thread(lambda: YouTube(url))
                self.yt.register_on_progress_callback(self.progress_func)
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

                self.video_with_audio = await ak.run_in_thread(
                    lambda: [
                        {
                            'qual': i.resolution,
                            'extension': i.mime_type,
                            'file_size': str(byte_to_mb(i.filesize))+' MB',
                            'itag': i.itag
                        } for i in self.yt.streams
                        .filter(file_extension='mp4')
                        .filter(progressive=True)
                    ]
                )

                self.video_without_audio = await ak.run_in_thread(
                    lambda: [
                        {
                            'qual': i.resolution,
                            'extension': i.mime_type,
                            'file_size': str(byte_to_mb(i.filesize))+' MB',
                            'itag': i.itag
                        } for i in self.yt.streams
                        .filter(file_extension='mp4')
                        .filter(progressive=False)
                    ]
                )

                self.audio_files = await ak.run_in_thread(
                    lambda: [
                        {
                            'qual': i.abr,
                            'extension': i.mime_type,
                            'file_size': str(byte_to_mb(i.filesize))+' MB',
                            'itag': i.itag
                        } for i in self.yt.streams
                        .filter(type='audio')
                        .filter(mime_type='audio/webm')
                    ]
                )

                self.current = 'download_options'
                self.current_screen.ids.image.source = self.thm_url
                self.current_screen.ids.title.text = self.title

                # to delete the last item
                self.video_without_audio.pop()

                option_layout = self.current_screen.ids.option_layout

                # Video with audio
                option_layout.add_widget(MDLabel(
                    text='Video(s) with Audio',
                    adaptive_height=True,
                    halign='center'
                ))

                for i in self.video_with_audio:
                    option_layout.add_widget(OptionListItem(
                        quality=i['qual'],
                        extension=i['extension'],
                        file_size=i['file_size'],
                        itag=i['itag']
                    ))

                # Videos without audio
                option_layout.add_widget(MDLabel(
                    text='Video(s) without Audio',
                    adaptive_height=True,
                    halign='center'
                ))

                for i in self.video_without_audio:
                    if i not in self.video_with_audio:
                        option_layout.add_widget(OptionListItem(
                            quality=i['qual'],
                            extension=i['extension'],
                            file_size=i['file_size'],
                            itag=i['itag']
                        ))

                # Audio files
                option_layout.add_widget(MDLabel(
                    text='Audio Files',
                    adaptive_height=True,
                    halign='center'
                ))

                for i in self.audio_files:
                    if i not in self.video_with_audio:
                        option_layout.add_widget(OptionListItem(
                            quality=i['qual'],
                            extension=i['extension'],
                            file_size=i['file_size'],
                            itag=i['itag']
                        ))

            except Exception as e:
                print(str(e))
                self.current = current_screen
        ak.start(some_task())

    def download(self, title):
        print(self.itag)
        print(self.res)
        print(title)
        self.previous_progress = 0
        current_screen = self.current

        async def some_task():

            stream = await ak.run_in_thread(lambda: self.yt.streams.get_by_itag(self.itag))
            self.file_size = stream.filesize
            print('Starting...')
            await ak.run_in_thread(lambda: stream.download(
                'output',
                filename=title + '_' + self.res,
                skip_existing=False
            ))
            print("done")
            self.show_toast('Downloaded!')
        ak.start(some_task())

    def change_screen(self, scrn):
        self.current = scrn

    def show_toast(self, message):
        toast(message)

    def progress_func(self, stream, chunk, bytes_remaining):
        size = stream.filesize
        bytes_downloaded = size - bytes_remaining

        self.liveprogress = (int)(bytes_downloaded/size * 100)

        if self.liveprogress > self.previous_progress:
            self.previous_progress = self.liveprogress
            print(self.liveprogress)

    # def percent(self, tem, total):
    #     perc = (float(tem) / float(total)) * float(100)
    #     return perc
