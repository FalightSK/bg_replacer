from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label

class controller_interface:
    def __init__(self):
        # Main layout
        self.controls_layout = BoxLayout(size_hint_x=0.3, orientation='vertical')

        # Grid layout for upper and lower bound slider
        self.lower_controls_layout = GridLayout(cols=3, padding=2)
        self.upper_controls_layout = GridLayout(cols=3, padding=2)

        # Sliders
        # Anya [49, 123, 124] [74, 255, 255]

        self.ColMin = Slider(min=0, max=180, value=49, orientation='vertical')
        self.SatMin = Slider(min=0, max=255, value=123, orientation='vertical')
        self.ValMin = Slider(min=0, max=255, value=124, orientation='vertical')
        self.ColMax = Slider(min=0, max=180, value=74, orientation='vertical')
        self.SatMax = Slider(min=0, max=255, value=255, orientation='vertical')
        self.ValMax = Slider(min=0, max=255, value=255, orientation='vertical')

        # Adding slider into grid layout
        self.lower_controls_layout.add_widget(Label(text='Hue', size_hint_y=0.3))
        self.lower_controls_layout.add_widget(Label(text='Sat', size_hint_y=0.3))
        self.lower_controls_layout.add_widget(Label(text='Val', size_hint_y=0.3))
        self.lower_controls_layout.add_widget(self.ColMin)
        self.lower_controls_layout.add_widget(self.SatMin)
        self.lower_controls_layout.add_widget(self.ValMin)

        self.upper_controls_layout.add_widget(Label(text='Hue', size_hint_y=0.3))
        self.upper_controls_layout.add_widget(Label(text='Sat', size_hint_y=0.3))
        self.upper_controls_layout.add_widget(Label(text='Val', size_hint_y=0.3))
        self.upper_controls_layout.add_widget(self.ColMax)
        self.upper_controls_layout.add_widget(self.SatMax)
        self.upper_controls_layout.add_widget(self.ValMax)

        # Slider Label
        self.lowerName = Label(text="Lowerbound", size_hint_y=0.2)
        self.upperName = Label(text="Upperbound", size_hint_y=0.2)

        # Box layout for dilation and erosion
        offset_lay = BoxLayout(size_hint_y=0.25, orientation='vertical')
        self.offset = Slider(min=-5, max=5, value=0, orientation='horizontal')
        offset_title = Label(text="Boarder Offset")
        offset_lay.add_widget(offset_title)
        offset_lay.add_widget(self.offset)

        self.update_layout()
        self.controls_layout.add_widget(offset_lay)

    def update_layout(self):
        self.controls_layout.add_widget(self.lowerName)
        self.controls_layout.add_widget(self.lower_controls_layout)
        self.controls_layout.add_widget(self.upperName)
        self.controls_layout.add_widget(self.upper_controls_layout)
    
