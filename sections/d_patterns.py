
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivy.uix.image import Image
from functools import partial
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
matplotlib.use('Agg')


class Patterns:
    def __init__(self):
        self.selected_pattern_visual = []

    def dict_pattern_sections(self):
        return {
            'NumNum': {
                'title': 'Numerical vs. Numerical Types',
                'visual_list': ['age vs. unit_price', 'age vs. loyalty_points', 'unit_price vs. loyalty_points'],
                'tab_visual': self.pattern_num_vs_num
            },
            'NumCat': {
                'title': 'Numerical vs. Categorical Types',
                'visual_list': ['purchased_via vs. age', 'order_returned vs. age', 'order_returned vs. unit_price'],
                'tab_visual': self.pattern_num_vs_cat
            },
            'CatCat': {
                'title': 'Categorical vs. Categorical Types',
                'visual_list': ['gender vs. purchased_via', 'gender vs. order_returned', 'purchased_via vs. order_returned'],
                'bar_colors': ['#FDBA74', '#7AB6D6', '#74FDBA', '#BA74FD'],
                'tab_visual': self.pattern_cat_vs_cat
            }
        }

    @staticmethod
    def get_patterns_home_label(sage_theme_dict):
        return MDLabel(
            text='please select a tab', halign='center', theme_text_color='Custom',
            text_color=sage_theme_dict.get('app_text'), font_style='H2', size_hint=[1, 0.2]
        )

    def get_pattern_tabs(self, sage_theme_dict, pattern_type):
        tab = TabbedPanelItem(text=pattern_type, color=sage_theme_dict.get('dn_gold'), background_down='')
        tab_layout = BoxLayout(orientation='vertical')
        tab_layout.clear_widgets()
        top_banner_box, bottom_banner_box = self.pattern_tabs_widgets(sage_theme_dict, pattern_type)
        tab_layout.add_widget(top_banner_box)
        tab_layout.add_widget(bottom_banner_box)
        tab.add_widget(tab_layout)
        return tab

    def pattern_tabs_widgets(self, sage_theme_dict, pattern_type):
        top_banner_box = BoxLayout(orientation='horizontal', size_hint=[1, 0.2])
        title = MDLabel(
            text=self.dict_pattern_sections().get(pattern_type).get('title'), halign='center', theme_text_color='Custom',
            text_color=sage_theme_dict.get('app_text'), font_style='H4'
        )
        top_banner_box.add_widget(title)
        bottom_banner_box = GridLayout(cols=2)
        check_banner_box = self.patterns_checkbox_widget(
            sage_theme_dict=sage_theme_dict,
            visual_list=self.dict_pattern_sections().get(pattern_type).get('visual_list')
        )
        bottom_banner_box.add_widget(check_banner_box)
        bottom_banner_box.add_widget(Image(opacity=0))
        return top_banner_box, bottom_banner_box

    def patterns_checkbox_widget(self, sage_theme_dict, visual_list):
        check_banner_box = GridLayout(rows=4, size_hint=[0.3, 1], padding=[15, 0, 0, 0])
        btn = Button(
            text='create graph', color=sage_theme_dict.get('app_button_text'), font_size='20sp',
            background_normal='', background_color=sage_theme_dict.get('app_button_background'),
            size_hint=[0.7, 0.2]
        )
        check_banner_box.add_widget(btn)
        for visual in visual_list:
            option_box = BoxLayout(orientation='horizontal', size_hint=[1, 1/4], padding=[20, 0, 0, 0])
            label = MDLabel(text=f'{visual}', size_hint=[2/3, 1], halign='left', valign='middle')
            checkbox = CheckBox(size_hint=[1/3, 1])
            checkbox.bind(active=partial(self.visual_is_selected, label))
            option_box.add_widget(label)
            option_box.add_widget(checkbox)
            check_banner_box.add_widget(option_box)
        return check_banner_box

    def visual_is_selected(self, label, value, instance):
        text = label.text
        self.selected_pattern_visual = []
        if value:
            self.selected_pattern_visual.append(text) if text not in self.selected_pattern_visual else self.selected_pattern_visual.remove(text)
            self.selected_pattern_visual = self.selected_pattern_visual

    @staticmethod
    def pattern_num_vs_num(assets_path, df, x, y):
        sns.set_theme(style='darkgrid')
        plt.figure(figsize=(8, 5))
        sns.scatterplot(data=df, x=x, y=y, c='#7AB6D6', s=200, alpha=0.7, palette='viridis')
        plt.title(f"{x} vs. {y}")
        plt.savefig(f"{assets_path}sage_pattern_numnum_{x}_{y}.png", bbox_inches='tight')
        plt.close()

    @staticmethod
    def pattern_num_vs_cat(assets_path, df, x, y):
        sns.set_theme(style='darkgrid')
        plt.figure(figsize=(8, 5))
        sns.boxplot(x=x, y=y, data=df)
        plt.title(f"{y} per {x}")
        plt.savefig(f"{assets_path}sage_pattern_numcat_{x}_{y}.png", bbox_inches='tight')
        plt.close()

    def pattern_cat_vs_cat(self, assets_path, df, x, y):
        sns.set(style="darkgrid")
        plt.figure(figsize=(8, 5))
        df.groupby([x, y]).size().unstack(fill_value=0).plot(kind='bar', stacked=True, color=self.dict_pattern_sections().get('CatCat').get('bar_colors'))
        plt.xticks(rotation=45)
        plt.title(f"{x} per {y}")
        plt.legend(loc='upper left', title='')
        plt.savefig(f"{assets_path}sage_pattern_catcat_{x}_{y}.png", bbox_inches='tight')
        plt.close()
