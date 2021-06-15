from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty


class OptionListItem(MDBoxLayout):
    quality = StringProperty()
    extension = StringProperty()
    file_size = StringProperty()
