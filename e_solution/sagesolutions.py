
from utilities.db_engines import DatabaseEngines
from e_solution.solution_analytics import SolutionAnalytics
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button


class SageSolutionsContent(BoxLayout):
    pass


class AmberContent(Screen):
    pass


class SageSolutionsApp(MDApp, DatabaseEngines, SolutionAnalytics):
    def __init__(self):
        super().__init__()
        self.section_nm = ''
        self.solution_title = 'SAGE data-360 - Solutions'

# ##############################################################
# ############################################################## solution sections
# ##############################################################

    def populate_solution_section(self, section_name):
        """
        :param section_name: sage-solution section name
        :return:
            - populates default tab with dynamic updates to section names
        """
        self.section_nm = section_name
        self.root.ids.screen_manager.current = 'solution_screen'
        default_tab_title = self.solution_sections_items().get('default_title').get(self.section_nm)
        self.root.ids.solution_section_title.text = default_tab_title
        self.root.ids.solutions_default_tab.text = section_name

    @staticmethod
    def solution_sections_items():
        d = {
            'default_title': {
                'regression': '''
    predict the revenue  for product
                ''',
                'classification': '''
    predict the likelihood of purchasing more than $ amount per month
                ''',
                'recommendation': '''
    recommend product in location
                '''
            }
        }
        return d

# ##############################################################
# ############################################################## populate prototype dropdown
# ##############################################################

    def prototype_list(self, prototype_button):
        """
        :param prototype_button: the parent button for prototype list
        :return:
            - opens the dropdown with list of all prototypes
        """
        dropdown = DropDown()
        for prototype in self.all_prototypes:
            btn = Button(
                text=prototype, color='gray', font_size='20sp', size_hint_y=None,
                background_normal='', background_color='e0e0e0'
            )
            btn.bind(on_release=lambda x: self.selected_prototype(prototype_button, x.text, dropdown))
            dropdown.add_widget(btn)
        dropdown.open(prototype_button)

    def selected_prototype(self, prototype_button, text, dropdown):
        """
        :param prototype_button: parent button for prototype list
        :param text: prototype name
        :param dropdown: widget for dropdown
        :return: when a prototype is selected:
            - the parent button changes to selected name
            - calls a function to fetch selected prototype widgets
            - closes the dropdown
        """
        prototype_button.text = text
        self.prototype_nm = text
        self.populate_prototype_tabs()
        dropdown.dismiss()

    def populate_prototype_tabs(self):
        """
        :return:
            - populates the selected prototype tabs after default tab
        """
        self.title = self.prototype_nm
        self.prototype_nm = self.prototype_nm.lower()
        prototype_sc = f'{self.prototype_nm}_home'
        self.root.ids.screen_manager.current = prototype_sc
        prototype_sections = list(self.get_prototypes_items().get(self.prototype_nm).get('dict')())
        for section in prototype_sections:
            tab = self.get_amber_section_tab(section)
            self.root.ids.screen_manager.get_screen(prototype_sc).ids.amber_tabs.add_widget(tab)

# ##############################################################
# ####################### TODO: review the rest in next version
# ##############################################################

# ############################################################## classifiers - logistic regression

    def evaluate_logistic_regression(self):
        self.screen_nm = self.root.ids.screen_manager.current
        self.root.ids.screen_manager.get_screen(self.screen_nm).ids.lr_results.clear_widgets()
        evaluation_table = self.table_model_stats_logistic_regression()
        self.root.ids.screen_manager.get_screen(self.screen_nm).ids.lr_results.add_widget(evaluation_table)
        pred_results = self.accuracy_pred_model_logistic_regression()
        ll = BoxLayout(orientation='horizontal', size_hint=[1, 0.2])
        self.root.ids.screen_manager.get_screen(self.screen_nm).ids.lr_results.add_widget(ll)
        lbd = MDLabel(
            text=f"    auc: {pred_results[0]} - - -  accuracy: {pred_results[1]} - - -  F1-score: {pred_results[2]}",
            font_size='150sp'
        )
        ll.add_widget(lbd)

# ############################################################## navbar top-left icons callback

    def callback_top_nav(self, x):
        self.root.ids.screen_manager.current = x
        self.screen_nm = x

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.title = self.solution_title
        return SageSolutionsContent()


if __name__ == '__main__':
    SageSolutionsApp().run()







