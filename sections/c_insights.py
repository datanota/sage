
from sections.c_insights_queries import InsightsQueries
from kivymd.uix.textfield import MDTextFieldRect
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivymd.uix.button import MDIconButton
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivy.uix.image import Image
from tabulate import tabulate
from functools import partial
import pandas as pd
import sqlite3
tabulate.PRESERVE_WHITESPACE = True


class Insights(InsightsQueries):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_db_default_tab(sage_theme_dict, img_source):
        default_tab = TabbedPanelItem(text='db', color=sage_theme_dict.get('dn_gold'), background_down='')
        default_tab_layout = BoxLayout(orientation='vertical')
        top_banner = MDLabel(
            text=f'Insights Q & A', halign='center', theme_text_color='Custom',
            text_color=sage_theme_dict.get('app_text'), font_style='H4', size_hint=[1, 0.1]
        )
        default_tab_layout.clear_widgets()
        default_tab_layout.add_widget(top_banner)
        default_tab_layout.add_widget(Image(source=img_source, allow_stretch=True))
        default_tab.add_widget(default_tab_layout)
        return default_tab

    def populate_insights_questions_tabs(self, sage_theme_dict, db_path, num, q, tip_dialog, theme_cls):
        insights_dict = self.dict_descriptive_insights(q)
        tab = TabbedPanelItem(text=f'Q{num}', color=sage_theme_dict.get('dn_gold'), background_down='')
        tab_parent_layout = BoxLayout(orientation='vertical')
        q_layout = BoxLayout(orientation='horizontal', padding='4dp', size_hint=[1, 0.4])
        q_layout.add_widget(MDLabel(text=insights_dict.get('Q'), halign='left', font_size='16sp'))
        q_key = MDIconButton(
            icon='key-variant', icon_size='44sp', theme_icon_color='Custom',
            icon_color=sage_theme_dict.get('dn_gold'), pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        q_key.bind(
            on_press=partial(
                tip_dialog, "Key:", insights_dict.get('A').get('sqlite'), theme_cls.primary_color
            )
        )
        q_layout.add_widget(q_key)
        tab_parent_layout.add_widget(q_layout)
        response_input_box = MDTextFieldRect(
            hint_text='  please answer the query question here', cursor_color=sage_theme_dict.get('input_box_foreground'),
            font_size='18dp'
        )
        tab_parent_layout.add_widget(response_input_box)
        btn = Button(
            text='run query', color=sage_theme_dict.get('app_button_text'), font_size='20sp',
            size_hint=[0.2, 0.2], pos_hint={'right': 1, 'center_y': 1}, background_normal='',
            background_color=sage_theme_dict.get('app_button_background')
        )
        query_result_widget = BoxLayout(orientation='vertical', padding=[0, 10, 0, 0])
        btn.bind(
            on_press=partial(self.run_insight_response_query, db_path, response_input_box, query_result_widget))
        tab_parent_layout.add_widget(btn)
        tab_parent_layout.add_widget(query_result_widget)
        tab.add_widget(tab_parent_layout)
        return tab

    def run_insight_response_query(self, *args):
        db_path = args[0]
        response_input_box = args[1]
        response_query = response_input_box.text
        query_result_widget = args[2]
        query_result_widget.clear_widgets()
        if response_query:
            try:
                returned_query, df, df_size = self.query_to_df_sqlite(db_path, response_query)
                if df_size != 0:
                    df_head = '======> The first few rows <======'
                else:
                    df_head = '======> df is empty <======'
                rt = MDLabel(
                    text=f'Total rows: {df_size}{df_head} \n\n {returned_query}',
                    font_size='16sp', halign='left'
                )
            except Exception as e:
                print(e)
                rt = MDLabel(text='Something went wrong. Please try again!', font_size='16sp', halign='left')
            query_result_widget.add_widget(rt)

    @staticmethod
    def query_to_df_sqlite(*args):
        db_path = args[0]
        response_query = args[1]
        db_conn = sqlite3.connect(f'{db_path}shopping.db')
        try:
            df = pd.read_sql_query(response_query, db_conn)
            query_return = tabulate(df.head(1), headers='keys', tablefmt='presto', showindex=False)
            df = df
            df_size = len(df)
        except pd.errors.DatabaseError as e:
            print(f"!!!!!!!!!!! ==> DatabaseError:\n {e}")
            query_return = 'try again!'
            df = None
            df_size = None
            db_conn.close()
        return query_return, df, df_size
