from logging import StrFormatStyle
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty, NumericProperty


class OptionListItem(MDBoxLayout):
    quality = StringProperty()
    extension = StringProperty()
    file_size = StringProperty()
    itag = NumericProperty()
