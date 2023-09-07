from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.uix.screen import Screen
from kivymd.uix.list import OneLineIconListItem
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
import gspread
from kivy.core.window import Window
from oauth2client.service_account import ServiceAccountCredentials

batch = ["2014-2018", "2015-2019", "2016-2020", "2017-2021", "2018-2022", "2019-2023", "2020-2024", "2021-2025", "2022-2026"]
gen = ["Male", "Female"]
KV = '''
<IconListItem>
 
    IconLeftWidget:
        icon: root.icon
 
MDScreen
 
    MDTextField:
        id: alname
        hint_text: "name"
        mode: "line"
        pos_hint:{'center_x': .5, 'center_y': .85}
        size_hint_x: None
        width: 200
        font_size: "18"

    MDTextField:
        id: alemail
        hint_text: "email"
        mode: "line"
        pos_hint:{'center_x': .5, 'center_y': .7}
        size_hint_x: None
        width: 200
        font_size: "18"

    MDTextField:
        id:phone
        hint_text: "phno"
        mode:"line"
        max_text_length: "10"
        pos_hint:{'center_x': .5, 'center_y': .55}
        size_hint_x: None
        width: 200
        font_size: "18"

    MDTextField:
        id: gender
        mode: "rectangle"
        pos_hint: {'center_x': .5, 'center_y': .4}
        size_hint_x: None
        width: "200"
        font_size: "18"
        hint_text: "Gender"
        helper_text: "Select your gender"
        icon: "calendar"
        icon_right: "Destination"
        icon_right_color: app.theme_cls.primary_color
        on_focus: if self.focus: app.gen_menu.open()
 
    MDTextField:
        id: batch
        mode: "rectangle"
        pos_hint: {'center_x': .5, 'center_y': .25}
        size_hint_x: None
        width: "200"
        font_size: "18"
        hint_text: "Batch"
        helper_text: "Select batch"
        icon: "calendar"
        icon_right: "Destination"
        icon_right_color: app.theme_cls.primary_color
        on_focus: if self.focus: app.make_menu.open()
 
    MDRectangleFlatIconButton:
        text: "Submit"
        icon: "content-save"
        text_color: app.theme_cls.primary_color
        line_color: app.theme_cls.primary_color
        pos_hint: {"center_x": .5, "center_y": .11}
        font_size: "20"
        on_release: app.add_alumni()
'''
 
class IconListItem(OneLineIconListItem):
    icon = StringProperty()
 
class Test(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        make_menu_items = [{"viewclass": "IconListItem", "icon": "", "height": dp(45), "text": f"{i}", "on_release": lambda x=f"{i}": self.set_make_item(x),} for i in batch]
        self.make_menu = MDDropdownMenu(caller=self.screen.ids.batch, items=make_menu_items, position="bottom", width_mult=4, max_height=dp(250))
        gen_menu_items = [{"viewclass": "IconListItem", "icon": "", "height": dp(45), "text": f"{i}", "on_release": lambda x=f"{i}": self.set_gen_item(x),} for i in gen]
        self.gen_menu = MDDropdownMenu(caller=self.screen.ids.gender, items=gen_menu_items, position="bottom", width_mult=4, max_height=dp(250))

    def set_make_item(self, selected_item):
        self.screen.ids.batch.text = selected_item
        self.make_menu.dismiss()

    def set_gen_item(self, selected_item):
        self.screen.ids.gender.text = selected_item
        self.gen_menu.dismiss()
 
    def build(self):
        Window.size = (480, 520)  # Set the window size here
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        return self.screen

    def on_start(self):
        # Initialize Google Sheets client
        json_keyfile_path = 'lokesh.json'
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
        self.gc = gspread.authorize(credentials)
        self.sheet = self.gc.open('lokesh testing').sheet1

    def add_alumni(self):
        name = self.screen.ids.alname.text
        email = self.screen.ids.alemail.text
        phone = self.screen.ids.phone.text
        batch = self.screen.ids.batch.text
        gender = self.screen.ids.gender.text

        if name and email and batch and gender:
            alumni_info = [name,email,phone,batch,gender]
            self.sheet.append_row(alumni_info)  # Append data to Google Sheet
            self.update_alumni_list()
            self.clear_input_fields()

    def update_alumni_list(self):
        # Fetch data from Google Sheet and update the alumni list in your Kivy app
        alumni_data = self.sheet.get_all_values()
       

    def clear_input_fields(self):
        self.screen.ids.alname.text = ""
        self.screen.ids.alemail.text = ""
        self.screen.ids.phone.text = ""
        self.screen.ids.batch.text = ""
        self.screen.ids.gender.text = ""

if __name__ == '__main__':
    Test().run()
