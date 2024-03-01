from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.graphics.texture import Texture

class functional_interface:
    def __init__(self, size=0.3):

        self.func_layout = BoxLayout(orientation='horizontal', size_hint_y=size)

        ## Main components
        self.bg_layout = BoxLayout(orientation='vertical')
        self.util_layout = BoxLayout(orientation='vertical')

        ## Sub components

        # bg sub
        self.bg_layout.add_widget(Label(text="Replace Mode"))
        bg_color_layout = GridLayout(cols=2)
        self.fullRes_btn = Button(text='fullRes')
        self.fitBg_btn = Button(text='fitBg')
        bg_color_layout.add_widget(self.fullRes_btn)
        bg_color_layout.add_widget(self.fitBg_btn)
        self.bg_layout.add_widget(bg_color_layout)

        self.bg_layout.add_widget(Label(text="BG-Mode"))
        bg_mode_layout = GridLayout(cols=2)
        self.img_btn = Button(text='Image')
        self.vid_btn = Button(text='Video')
        bg_mode_layout.add_widget(self.img_btn)
        bg_mode_layout.add_widget(self.vid_btn)
        self.bg_layout.add_widget(bg_mode_layout)

        self.func_layout.add_widget(self.bg_layout)

        # util sub
        ip_layout = GridLayout(cols=2)
        ip_layout.add_widget(Label(text='Source-IP', size_hint_x=None, width=100))
        self.Ip_input = TextInput(text='172.21.16.1:8000', multiline=False)
        ip_layout.add_widget(self.Ip_input)
        self.util_layout.add_widget(ip_layout)
        
        self.upload_btn = Button(text='Upload Source')
        self.util_layout.add_widget(self.upload_btn)

        self.util_layout.add_widget(Label(text='Chroma-Source'))
        re_mode = GridLayout(cols=2)
        self.ccam_btn = Button(text='Cam')
        self.cvid_btn = Button(text='Vid')
        re_mode.add_widget(self.ccam_btn)
        re_mode.add_widget(self.cvid_btn)
        self.util_layout.add_widget(re_mode)

        self.record_btn = Button(text='Start Recording')
        self.util_layout.add_widget(self.record_btn)

        self.func_layout.add_widget(self.util_layout)

        # color Range
        self.Color_range = Image(size_hint_x=0.5)
        self.func_layout.add_widget(self.Color_range)

    def set_btn_func(self, **kwargs):

        buttons = []
        funcs = []

        for k, d in kwargs.items():
            if 'btn' in k:
                buttons.append(d)
            elif 'func' in k:
                funcs.append(d)

        for btn, f in zip(buttons, funcs):
            btn.bind(on_press=f)
    
    def update_chart(self, frame, img):
        texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
        texture.blit_buffer(frame, colorfmt='bgr', bufferfmt='ubyte')
        self.Color_range.texture = texture