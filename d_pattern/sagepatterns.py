
from d_pattern.pattern_analytics import PatterAnalytics
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanelItem


class SagePatternsContent(Screen):
    pass


class SagePatternsApp(MDApp, PatterAnalytics):
    def __init__(self):
        super().__init__()
        self.section_nm = ''

# ############################################################## pattern sections dictionary

    def pattern_sections_items(self, section_nm):
        section_dict = self.dict_pattern_sections()
        title = section_dict.get(section_nm).get('title')
        default_graph = section_dict.get(section_nm).get('default_graph')
        default_title = section_dict.get(section_nm).get('default_title')
        tabs_list = section_dict.get(section_nm).get('tabs')
        return title, default_graph, default_title, tabs_list

# ############################################################## populate pattern sections

    def populate_pattern_section(self, section_name):
        """
        :param section_name: pattern section name
        :return:
            - populates default tab with dynamic updates to section names
            - populates section concepts in remaining tabs
        """
        self.section_nm = section_name
        self.root.ids.screen_manager.current = 'pattern_screen'
        title, default_graph, default_title, tabs_list = self.pattern_sections_items(self.section_nm)
        self.fetch_patterns_default_tab(title, default_graph, default_title)
        for concept in tabs_list:
            tab = self.populate_pattern_tabs(concept)
            self.root.ids.pattern_tabs.add_widget(tab)

# ############################################################## default tab layout

    def fetch_patterns_default_tab(self, title, default_graph, default_title):
        self.root.ids.patterns_default_tab.text = default_title
        self.root.ids.pattern_section_title.text = title
        graph_source = self.get_assets_path(default_graph)
        self.root.ids.pattern_section_default_graph.source = graph_source

# ############################################################## concept tabs layout

    @staticmethod
    def populate_pattern_tabs(concept):
        tab = TabbedPanelItem(text=concept, color=[215 / 255, 163 / 255, 9 / 255], background_down='')
        tab_parent_layout = BoxLayout(orientation='vertical')
        tab.add_widget(tab_parent_layout)
        return tab

# ############################################################## navbar top-left icons callback

    def callback_top_nav(self, x):
        self.root.ids.screen_manager.current = x

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.title = 'SAGE data-360 - Patterns'
        return SagePatternsContent()


if __name__ == '__main__':
    SagePatternsApp().run()







