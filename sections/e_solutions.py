
from kivymd.uix.button import MDFillRoundFlatButton


class Solutions:
    def __init__(self):
        pass

    @staticmethod
    def solutions_home_buttons(text, sage_theme_dict):
        btn = MDFillRoundFlatButton(
            text=text, font_size='20sp', size_hint=[0.97, None],
            md_bg_color=sage_theme_dict.get('app_button_background')
        )
        return btn
