
from c_insights.queries.levels.questions_level1 import LevelOneQuestions
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.uix.button import MDIconButton
from functools import partial
import datetime


class SageInsightsContent(BoxLayout):
    pass


class Level1(Screen):
    pass


class Level2(Screen):
    pass


class SageInsightsApp(MDApp, LevelOneQuestions):
    def __init__(self):
        super().__init__()
        self.screen_nm = ''
        self.q = ''
        self.q_re_run = ''
        self.response_input = None
        self.r_box = BoxLayout(orientation='vertical')

# ############################################################## database check

    def check_db_schema(self):
        self.screen_nm = self.root.ids.screen_manager.current
        print(self.screen_nm)
        query = self.root.ids.screen_manager.get_screen(self.screen_nm).ids.query_box.text
        query_return, df, df_size = self.run_query(query)
        rt = MDLabel(text=f'Total rows: {df_size}\n The first few rows: \n\n {query_return}', font_size='16sp', halign='left')
        self.root.ids.screen_manager.get_screen(self.screen_nm).ids.query_results.clear_widgets()
        self.root.ids.screen_manager.get_screen(self.screen_nm).ids.query_results.add_widget(rt)
        btn = Button(text='save query', color=[211/255, 217/255, 208/255], font_size='20sp',
                     size_hint=[0.2, 0.25], pos_hint={'right': 1,'center_y': 1}, background_normal='',
                     background_color=[69/255, 92/255, 100/255])
        self.root.ids.screen_manager.get_screen(self.screen_nm).ids.query_results.add_widget(btn)
        btn.bind(on_press=partial(self.save_query_return, df))

    def save_query_return(self, *args):
        self.screen_nm = self.root.ids.screen_manager.current
        timestamp_now = datetime.datetime.now().strftime('%Y%m%d')
        file_name = f'saved_{timestamp_now}.csv'
        df = args[0]
        self.root.ids.screen_manager.get_screen(self.screen_nm).ids.query_results.clear_widgets()
        saved_file = MDLabel(
            text=f"Query results is saved here: \n\n {self.saved_queries_path.split('sage')[1]}",
            font_size='16sp', halign='center'
        )
        self.root.ids.screen_manager.get_screen(self.screen_nm).ids.query_results.add_widget(saved_file)
        df.to_csv(f'{self.saved_queries_path}{file_name}', index=False)

# ############################################################## questions

    def insight_questions_screen(self, q):
        self.screen_nm = self.root.ids.screen_manager.current
        self.q = q
        self.question_set(q).clear_widgets()
        top_box = BoxLayout(orientation='horizontal', padding='4dp', size_hint=[1, 0.4])
        self.question_set(q).add_widget(top_box)
        question = MDLabel(text=self.insight_sets(q).get('Q'), halign='left', font_size='16sp')
        top_box.add_widget(question)

        q_key = MDIconButton(
            icon='key-variant', icon_size='44sp', theme_icon_color='Custom',
            icon_color=[215/255, 163/255, 9/255], pos_hint={'center_x': 0.5,'center_y': 0.7}
        )
        q_key.bind(
            on_press=partial(
                self.tip_dialog, 'Key:', self.insight_sets(self.q).get('A'), self.theme_cls.primary_color
            )
        )
        top_box.add_widget(q_key)

        m = MDTextFieldRect(hint_text='please answer the query question here')
        self.response_input = m
        self.question_set(q).add_widget(m)
        btn = Button(
            text='run query', color=[211/255, 217/255, 208/255], font_size='20sp',
            size_hint=[0.2, 0.2], pos_hint={'right': 1,'center_y': 1}, background_normal='',
            background_color=[69/255, 92/255, 100/255]
        )
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
            rt = MDLabel(
                text=f'Total rows: {df_size}\n The first 5 rows: \n\n {t}',
                font_size='16sp', halign='left'
            )
            self.r_box.add_widget(rt)
        self.q_re_run = self.q

    def question_set(self, q):
        q_dict = {
            'q1': self.root.ids.screen_manager.get_screen(self.screen_nm).ids.q1,
            'q2': self.root.ids.screen_manager.get_screen(self.screen_nm).ids.q2,
            'q3': self.root.ids.screen_manager.get_screen(self.screen_nm).ids.q3,
            'q4': self.root.ids.screen_manager.get_screen(self.screen_nm).ids.q4,
            'q5': self.root.ids.screen_manager.get_screen(self.screen_nm).ids.q5,
            'q6': self.root.ids.screen_manager.get_screen(self.screen_nm).ids.q6,
            'q7': self.root.ids.screen_manager.get_screen(self.screen_nm).ids.q7,
            'q8': self.root.ids.screen_manager.get_screen(self.screen_nm).ids.q8,
            'q9': self.root.ids.screen_manager.get_screen(self.screen_nm).ids.q9,
            'q10': self.root.ids.screen_manager.get_screen(self.screen_nm).ids.q10
        }
        return q_dict.get(q)

# ############################################################## navbar top-left icons callback

    def callback_top_nav(self, x):
        self.root.ids.screen_manager.current = x
        self.screen_nm = x

# ##############################################################

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.title = 'SAGE data-360 - Insights'
        return SageInsightsContent()


if __name__ == '__main__':
    SageInsightsApp().run()







