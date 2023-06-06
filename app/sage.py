
from utilities.data_generation import DataGeneration
from utilities.db_generation import DbGeneration
from utilities.insights import Insights
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDIconButton
from functools import partial
import webbrowser
import datetime

from kivy.uix.button import Button


class SageContent(BoxLayout):
    pass


class SageApp(MDApp, DataGeneration, DbGeneration, Insights):
    def __init__(self):
        super().__init__()
        self.q = ''
        self.q_re_run = ''
        self.response_input = None
        self.r_box = BoxLayout(orientation='vertical')

# ############################################################## insights

    def test_run_queries(self):
        query = self.root.ids.query_box.text
        query_return, df, df_size = self.run_query(query)
        rt = MDLabel(text=f'Total rows: {df_size}\n The first few rows: \n\n {query_return}', font_size='16sp', halign='left')
        self.root.ids.query_results.clear_widgets()
        self.root.ids.query_results.add_widget(rt)
        btn = Button(text='save query', color=[211/255, 217/255, 208/255], font_size='20sp',
                     size_hint=[0.2, 0.25], pos_hint={'right': 1,'center_y': 1}, background_normal='',
                     background_color=[69/255, 92/255, 100/255])
        self.root.ids.query_results.add_widget(btn)
        btn.bind(on_press=partial(self.save_query_return, df))

    def save_query_return(self, *args):
        timestamp_now = datetime.datetime.now().strftime('%Y%m%d')
        file_name = f'saved_{timestamp_now}.csv'
        df = args[0]
        self.root.ids.query_results.clear_widgets()
        saved_file = MDLabel(text=f'Query results is saved here: \n\n {self.data_path}{self.q_files}{file_name}',
                             font_size='16sp', halign='center')
        self.root.ids.query_results.add_widget(saved_file)
        df.to_csv(f'{self.q_files_path}{file_name}', index=False)

    def insight_questions_screen(self, q):
        self.q = q
        self.question_set(q).clear_widgets()
        top_box = BoxLayout(orientation='horizontal', padding='4dp', size_hint=[1, 0.4])
        self.question_set(q).add_widget(top_box)
        question = MDLabel(text=self.insight_sets(q).get('Q'), halign='left', font_size='16sp')
        top_box.add_widget(question)
        q_key = MDIconButton(icon='key-variant', icon_size='44sp', theme_icon_color='Custom',
                             icon_color=[215/255, 163/255, 9/255], pos_hint={'center_x': 0.5,'center_y': 0.7})
        q_key.bind(on_press=partial(self.tip_dialog, 'Key:', self.insight_sets(self.q).get('A')))
        top_box.add_widget(q_key)
        m = MDTextFieldRect(hint_text='please answer the query question here')
        self.response_input = m
        self.question_set(q).add_widget(m)
        btn = Button(text='run query', color=[211/255, 217/255, 208/255], font_size='20sp',
                     size_hint=[0.2, 0.2], pos_hint={'right': 1,'center_y': 1}, background_normal='',
                     background_color=[69/255, 92/255, 100/255])
        self.question_set(q).add_widget(btn)
        btn.bind(on_press=partial(self.insight_response_query))

    def insight_response_query(self, instance):
        if self.q_re_run == self.q:
            self.r_box.clear_widgets()
        else:
            if self.q_re_run == '':
                self.question_set(self.q).add_widget(self.r_box)
            else:
                self.r_box.clear_widgets()
                self.question_set(self.q_re_run).remove_widget(self.r_box)
                self.question_set(self.q).add_widget(self.r_box)
        response_query = self.response_input.text
        if response_query:
            t, df, df_size = self.run_query(response_query)
            rt = MDLabel(text=f'Total rows: {df_size}\n The first 5 rows: \n\n {t}', font_size='16sp', halign='left')
            self.r_box.add_widget(rt)
        self.q_re_run = self.q

    def question_set(self, q):
        q_dict = {'q1': self.root.ids.q1, 'q2': self.root.ids.q2, 'q3': self.root.ids.q3,
                  'q4': self.root.ids.q4, 'q5': self.root.ids.q5, 'q6': self.root.ids.q6,
                  'q7': self.root.ids.q7, 'q8': self.root.ids.q8, 'q9': self.root.ids.q9}
        return q_dict.get(q)

# ############################################################## build a database

    def create_database(self):
        self.df_to_db()
        lbd = MDLabel(text=f'database is created: {self.data_path}', font_size='80sp')
        self.root.ids.db_outcome.clear_widgets()
        self.root.ids.db_outcome.add_widget(lbd)

# ############################################################## data generation
    def data_input_check(self):
        c = self.root.ids.num_customers.text
        p = self.root.ids.num_products.text

        lbc = MDLabel(text=f'Total number of customers: {c}', font_size='40sp')
        lbp = MDLabel(text=f'Total number of products: {p}', font_size='40sp')

        btn = Button(
                text='save data', color='000000', font_size='20sp', background_color='85ADA3',
                background_normal='', size_hint=(0.9, 0.75)
            )
        self.root.ids.data_input_check.clear_widgets()
        self.root.ids.data_input_check.add_widget(lbc)
        self.root.ids.data_input_check.add_widget(lbp)
        self.root.ids.data_input_check.add_widget(btn)
        btn.bind(on_press=partial(self.save_to_file_generated_data, c, p))

    def save_to_file_generated_data(self, *args):
        cust_num = args[0]
        prd_num = args[1]
        self.generate_data(cust_num, prd_num)
        lbd = MDLabel(text=f'data is saved in dir: {self.data_path}{self.data_files}', font_size='60sp')
        self.root.ids.data_preview.add_widget(lbd)

# ############################################################## navbar top-left icons callback

    def callback_top_nav(self, x):
        self.root.ids.screen_manager.current = x

# ############################################################### navbar top-right tip

    def tip_dialog(self, *args):
        title = args[0]
        tip = args[1]
        dialog = MDDialog(
            title=title,
            text='[color=222222]' + tip,
            buttons=[
                MDFlatButton(
                    text='Dismiss',
                    theme_text_color='Custom',
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: dialog.dismiss()
                )
            ],
        )
        dialog.open()

# ############################################################### screenshot

    @staticmethod
    def sage_ss():
        img_nm = datetime.datetime.now().strftime("%Y_%m%d%H%M_")
        Window.screenshot(name=img_nm + '.png')

# ############################################################## demo

    @staticmethod
    def dn_sage_demo():
        webbrowser.open('https://www.datanota.com/sage')

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        return SageContent()


if __name__ == '__main__':
    SageApp().run()







