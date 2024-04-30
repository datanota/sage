
from utilities.db_engines import DatabaseEngines
from c_insight.insights_descriptive import DescriptiveInsights
from c_insight.insights_comparative import ComparativeInsights
from c_insight.insights_derived import DerivedInsights
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivy.uix.image import Image
from functools import partial
import datetime


class SageInsightContent(BoxLayout):
    pass


class SageInsightApp(MDApp, DatabaseEngines, DescriptiveInsights, ComparativeInsights, DerivedInsights):
    def __init__(self):
        super().__init__()
        self.q = ''
        self.section_nm = ''

# ############################################################## section screen

    def get_section_screen(self, section_name):
        """
        :param section_name: sage-insights is categorized in sections (e.g. descriptive)
        :return:
            - transitions to generic screen for sections
            - clears possible existing widgets
            - calls default function to create default tab with db schema and given section name
            - calls questions function to populate the question tabs: 10 questions (1-11), answer key,
              response box, run button and save button if needed
        """
        self.section_nm = section_name
        self.root.ids.screen_manager.current = 'section_screen'
        self.root.ids.q_tabs.clear_tabs()
        default_tab = self.populate_section_default_tab()
        self.root.ids.q_tabs.add_widget(default_tab)
        self.root.ids.q_tabs.switch_to(self.root.ids.q_tabs.tab_list[0])
        for num in range(1, 11):
            self.q = f"q{num}"
            tab = self.populate_section_question_tabs()
            self.root.ids.q_tabs.add_widget(tab)

# ############################################################## default tab layout

    def populate_section_default_tab(self):
        """
        :return: default tab with dynamic update to insights section names
        """
        default_tab = TabbedPanelItem(text='schema', color=[215 / 255, 163 / 255, 9 / 255], background_down='')
        default_tab_layout = GridLayout(rows=2)
        top_banner = MDLabel(
            text=f'{self.section_nm} insights', halign='center', theme_text_color='Custom',
            text_color=[81 / 255, 81 / 255, 81 / 255], font_style='H4', size_hint=[1, 0.1]
        )
        default_tab_layout.clear_widgets()
        default_tab_layout.add_widget(top_banner)
        default_image = self.get_assets_path('sage_2_db/db_schema_shopping.png')
        default_tab_layout.add_widget(Image(source=default_image, allow_stretch=True))
        default_tab.add_widget(default_tab_layout)
        return default_tab

# ############################################################## question tabs layout

    def populate_section_question_tabs(self):
        """
        :return:
            - calls sage-insights section dictionary of questions and per-engine answers from respective section modules
            - fetches dictionary per-engine answer for key widget
            - adds a box to answer the query
            - adds the run button which calls the query returned response function
            - adds a placeholder boxlayout (returned_results_boxlayout) for returned response function
        """
        insights_dict = self.dict_section_insights()
        tab = TabbedPanelItem(text=self.q.upper(), color=[215 / 255, 163 / 255, 9 / 255], background_down='')
        tab_parent_layout = BoxLayout(orientation='vertical')
        q_layout = BoxLayout(orientation='horizontal', padding='4dp', size_hint=[1, 0.4])
        q_layout.add_widget(MDLabel(text=insights_dict.get('Q'), halign='left', font_size='16sp'))
        q_key = MDIconButton(
            icon='key-variant', icon_size='44sp', theme_icon_color='Custom',
            icon_color=[215 / 255, 163 / 255, 9 / 255], pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        q_key.bind(
            on_press=partial(
                self.tip_dialog, "Key:", insights_dict.get('A').get(self.engine), self.theme_cls.primary_color
            )
        )
        q_layout.add_widget(q_key)
        tab_parent_layout.add_widget(q_layout)
        given_answer_widget = MDTextFieldRect(
            hint_text='  please answer the query question here', cursor_color=[16/255, 16/255, 241/255], font_size='18dp'
        )
        tab_parent_layout.add_widget(given_answer_widget)
        btn = Button(
            text='run query', color=[211 / 255, 217 / 255, 208 / 255], font_size='20sp',
            size_hint=[0.2, 0.2], pos_hint={'right': 1, 'center_y': 1}, background_normal='',
            background_color=[69 / 255, 92 / 255, 100 / 255]
        )
        returned_results_boxlayout = BoxLayout(orientation='vertical', padding=[0, 10, 0, 0])
        btn.bind(on_press=partial(self.insight_response_query, given_answer_widget, returned_results_boxlayout))
        tab_parent_layout.add_widget(btn)
        tab_parent_layout.add_widget(returned_results_boxlayout)
        tab.add_widget(tab_parent_layout)
        return tab

    def dict_section_insights(self):
        insights_dict = None
        if self.section_nm == 'descriptive':
            insights_dict = self.dict_descriptive_insights(self.q)
        if self.section_nm == 'comparative':
            insights_dict = self.dict_comparative_insights(self.q)
        if self.section_nm == 'derived':
            insights_dict = self.dict_derived_insights(self.q)
        return insights_dict

# ############################################################## query returned answer

    def insight_response_query(self, *args):
        """
        :param args:
            - args[0]: given_answer_widget: the space to write the query answer text
            - args[1]: returned_results_boxlayout to add returned df and save button if df not empty
        :return:
            - fetches the given answer text
            - checks if there is a given answer, then runs the per-engine query answer
            - checks if df is not empty, then shows the first few rows, adds save button and calls save function
            - if df is empty, does not add save button
        """
        response_query = args[0].text
        returned_results_boxlayout = args[1]
        returned_results_boxlayout.clear_widgets()
        if response_query:
            try:
                t, df, df_size = self.dict_engines_functions().get(self.engine)[1](response_query)
                if df_size != 0:
                    df_head = '======> The first few rows <======'
                    btn = Button(
                        text='save data', color=[211 / 255, 217 / 255, 208 / 255], font_size='20sp',
                        size_hint=[0.2, 0.2], pos_hint={'right': 1, 'center_y': 1}, background_normal='',
                        background_color=[69 / 255, 92 / 255, 100 / 255]
                    )
                    btn.bind(on_press=partial(self.save_query_return, df, returned_results_boxlayout))
                    returned_results_boxlayout.add_widget(btn)
                else:
                    df_head = '======> df is empty <======'
                rt = MDLabel(
                    text=f'Total rows: {df_size}{df_head} \n\n {t}',
                    font_size='16sp', halign='left'
                )
            except Exception as e:
                print(e)
                rt = MDLabel(text='Something went wrong. Please try again!', font_size='16sp', halign='left')
            returned_results_boxlayout.add_widget(rt)

# ############################################################## save query answer data

    def save_query_return(self, *args):
        """
        :param args:
            arg[0]: query returned response as a df
        :return:
            - clears all widgets in returned_results_boxlayout
            - gives a name to saved file based on timestamp YearMonthDay_HourMinuteSecond
            - creates a directory for saved file if not exists
        """
        df = args[0]
        returned_results_boxlayout = args[1]
        returned_results_boxlayout.clear_widgets()
        timestamp_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f'saved_{timestamp_now}.csv'
        saved_file = MDLabel(
            text=f"Query results file {file_name} is saved here: \n\n {self.saved_queries_path.split('sage')[1]}",
            font_size='16sp', halign='center'
        )
        self.create_dir_if_not_exists(self.saved_queries_path)
        df.to_csv(f'{self.saved_queries_path}{file_name}', index=False)
        returned_results_boxlayout.add_widget(saved_file)

# ############################################################## navbar top-left icons callback

    def callback_top_nav(self, x):
        self.root.ids.screen_manager.current = x

# ###############################################################

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.title = 'SAGE data-360 - Insights'
        return SageInsightContent()


if __name__ == '__main__':
    SageInsightApp().run()

