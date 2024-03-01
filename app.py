import cv2
import numpy as np
from tools.ChromaKey import *
from Gui.controller import controller_interface
from Gui.functional import functional_interface

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.clock import Clock
from kivy.graphics.texture import Texture

import os
import shutil

class KivyCVApp(App):

    def build(self):

        # Root layout
        root_layout = BoxLayout(orientation='horizontal')

        # Container for main layout
        main_layout = BoxLayout(orientation='vertical')

        # Image widget to display video frames
        self.img1 = Image()
        main_layout.add_widget(self.img1)

        # Initiate functional layout
        self.func_layout = functional_interface(size=0.3)
        self.func_layout.set_btn_func(
            btn1 = self.func_layout.fullRes_btn,
            btn2 = self.func_layout.fitBg_btn,
            btn3 = self.func_layout.img_btn,
            btn4 = self.func_layout.vid_btn,
            btn5 = self.func_layout.upload_btn,
            btn6 = self.func_layout.record_btn,
            btn7 = self.func_layout.ccam_btn,
            btn8 = self.func_layout.cvid_btn,
            func1 = self.on_replace_mode,
            func2 = self.on_replace_mode,
            func3 = self.on_bg_mode,
            func4 = self.on_bg_mode,
            func5 = self.on_upload,
            func6 = self.on_record,
            func7 = self.on_source_type,
            func8 = self.on_source_type
        )
        self.func_layout.Ip_input.bind(on_text_validate=self.on_enter_ip)
        main_layout.add_widget(self.func_layout.func_layout)

        # Adding func_layout to the root
        root_layout.add_widget(main_layout)

        # Initiate controller layout GUI
        self.controls_layout = controller_interface()
        # Add the controls layout to the root layout
        root_layout.add_widget(self.controls_layout.controls_layout)

        # Initiate variable for Chormakey
        self.colRange = [40, 65]
        self.SatRange = [0, 255]
        self.ValRange = [0, 255]
        self.lowerHSV = [self.colRange[0], self.SatRange[0], self.ValRange[0]]
        self.upperHSV = [self.colRange[1], self.SatRange[1], self.ValRange[1]]

        self.is_vid = 0
        self.replace = cv2.imread(os.path.join(os.getcwd(), 'src', 'replace_img.png'))

        self.is_rec = 0
        self.recoder = None

        self.source_type_cam = 1

        self.is_fullRes = 1

        # HS color chart
        self.chart = cv2.imread(os.path.join(os.getcwd(), 'src', 'HSV_chart.png'))
        circle_mask = np.zeros(self.chart.shape, dtype=np.uint8)
        cv2.circle(
            circle_mask, 
            (int(self.chart.shape[1]/2), int(self.chart.shape[0]/2)),
            int(self.chart.shape[0]/2),
            [255, 255, 255],
            -1
            )
        self.chart = cv2.bitwise_and(self.chart, circle_mask, mask=None)

        # Setup video capture
        self.capture = cv2.VideoCapture()

        # Schedule the update of the video
        Clock.schedule_interval(self.update, 1.0/30.0)

        # Update slider value overetime
        Clock.schedule_interval(self.update_bound, 1.0/30.0)

        return root_layout

    def update(self, dt):
        # Read frame from capture
        ret, frame = self.capture.read()

        if ret:
            replace = None
            if self.is_vid:
                # Restart the Video if it reaches the end
                _, holder = self.replace.read()
                if _:
                    replace = holder
                else:
                    self.replace.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    _, replace = self.replace.read()
            else:
                replace = self.replace
            
            replace = cv2.resize(replace, (frame.shape[1], frame.shape[0]))

            # Apply ChromaKey function
            res = RemoveBG(
                frame, 
                np.array(self.upperHSV, dtype=np.int16), 
                np.array(self.lowerHSV, dtype=np.int16), 
                replace,
                int(self.controls_layout.offset.value),
                self.is_fullRes
                )

            if self.is_rec:
                self.recoder.write(res)
            
            # Convert image to texture
            buf = cv2.flip(res, 0).tobytes()
            # Add chromaKey
            texture = Texture.create(size=(res.shape[1], res.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img1.texture = texture
        
        # Display the masked color range
        buf = ShowSeletected(self.chart, np.array(self.upperHSV, dtype=np.int16), np.array(self.lowerHSV, dtype=np.int16))
        self.func_layout.update_chart(buf, self.chart)
    
    def update_bound(self, dt):
        self.colRange = [self.controls_layout.ColMin.value, self.controls_layout.ColMax.value]
        self.SatRange = [self.controls_layout.SatMin.value, self.controls_layout.SatMax.value]
        self.ValRange = [self.controls_layout.ValMin.value, self.controls_layout.ValMax.value]
        self.lowerHSV = [self.colRange[0], self.SatRange[0], self.ValRange[0]]
        self.upperHSV = [self.colRange[1], self.SatRange[1], self.ValRange[1]]

    def on_replace_mode(self, instance):
        if instance.text == 'fullRes':
            self.is_fullRes = 1
        elif instance.text == 'fitBg':
            self.is_fullRes = 0

    def on_bg_mode(self, instance):
        if instance.text == 'Image':
            self.is_vid = 0
            self.replace = cv2.imread(os.path.join(os.getcwd(), 'src', 'replace_img.png'))
        elif instance.text == 'Video':
            self.is_vid = 1
            self.replace = cv2.VideoCapture(os.path.join(os.getcwd(), 'src', 'replace_vid.mp4'))

    def on_upload(self, instance):
        # Layout for the content of the popup
        content = BoxLayout(orientation='vertical')

        # FileChooser to select a file
        self.filechooser = FileChooserListView(size_hint_y=0.9)

        # Button to confirm the file selection
        select_button = Button(text='Select', size_hint_y=0.1)
        select_button.bind(on_press=self.select_file)

        content.add_widget(self.filechooser)
        content.add_widget(select_button)

        # Popup widget
        self.popup = Popup(title='Choose a file', content=content, size_hint=(0.9, 0.9))
        self.popup.open()

    def select_file(self, instance):
        # Get the selected file path from the FileChooser
        if self.filechooser.selection:
            selected_path = self.filechooser.selection[0]
            path_list = selected_path.split('/')
            filename = path_list[len(path_list)-1].split('.')
            filetype = filename[len(filename)-1]

            if 'png' in filetype:
                shutil.copyfile(selected_path, os.path.join(os.getcwd(), 'src', 'replace_img.png'))
            elif 'mp4' in filetype:
                shutil.copyfile(selected_path, os.path.join(os.getcwd(), 'src', 'replace_vid.mp4'))

        # Close the popup
        self.popup.dismiss()
    
    def on_source_type(self, instance):
        if instance.text == 'Cam':
            self.source_type_cam = 1
        elif instance.text == 'Vid':
            self.source_type_cam = 0
        print('enter')

    def on_enter_ip(self, instance):
        if self.source_type_cam:
            self.capture = cv2.VideoCapture()
            self.capture.open('http://' + self.func_layout.Ip_input.text + '/')
        else:
            # Input must be abs path to video
            self.capture = cv2.VideoCapture(os.path.join(os.getcwd(), 'src', self.func_layout.Ip_input.text))

    def on_record(self, instance):
        self.is_rec = not self.is_rec
        if self.is_rec:
            self.recoder = cv2.VideoWriter(
                os.path.join(os.getcwd(),'result.mp4'),
                cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 
                30.0, 
                (int(self.capture.get(3)), int(self.capture.get(4)))
                )
            print('strat recording')
        else:
            self.recoder.release()
            print('stop recording')

    def on_stop(self):
        # Release the capture when the app is closed
        print(self.upperHSV)
        print(self.lowerHSV)
        self.capture.release()

if __name__ == '__main__':
    KivyCVApp().run()