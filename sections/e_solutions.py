
from sections.e_solutions_amber import Amber
from kivymd.uix.button import MDFillRoundFlatButton


class Solutions(Amber):
    def __init__(self):
        super().__init__()

    @staticmethod
    def solutions_home_buttons(text, sage_theme_dict):
        btn = MDFillRoundFlatButton(
            text=text, font_size='20sp', size_hint=[0.97, None],
            md_bg_color=sage_theme_dict.get('app_button_background')
        )
        return btn

    def dict_solutions(self):
        return {
            'Amber': self.dict_amber
        }
