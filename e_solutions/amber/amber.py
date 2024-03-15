
from kivy.core.window import Window
from e_solutions.amber.assets.amber_analytics import AmberAnalytics
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import datetime


class AmberContent(BoxLayout):
    pass


class AmberApp(MDApp, AmberAnalytics):
    def __init__(self):
        super().__init__()
        self.df = self.get_df_available_stocks_data()

    # ############################################################### generic

    @staticmethod
    def dn_ss():
        img_nm = datetime.datetime.now().strftime("%Y_%m%d%H%M_")
        Window.screenshot(name=img_nm + '.png')

    def tip_dialog(self, title, tip):
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

    # ############################################################## decision helper -- buy

    def show_investment_recommendations(self):
        row_data = []
        inv_dollar = self.root.ids.dm_buy_invest.text
        if inv_dollar == '':
            inv_dollar = 1000.0
        else:
            inv_dollar = float(inv_dollar)
        buy_list = self.get_investment_recommendations(inv_dollar, self.df)
        for i in buy_list:
            row_data.append(tuple(i))
        table = MDDataTable(
            use_pagination=True,
            column_data=[
                ('stock', dp(25)),
                ('investing_units', dp(45)),
                ('current_price', dp(45)),
                ('percent_change', dp(35))
            ],
            row_data=row_data
        )
        self.root.ids.dm_buy_rec_results.clear_widgets()
        self.root.ids.dm_buy_rec_results.add_widget(table)
        self.df = self.get_df_available_stocks_data()

    # ############################################################## decision helper -- sell

    def show_cash_recommendations(self):
        row_data = []
        sell_list = self.get_cash_recommendations(self.df)
        for i in sell_list:
            row_data.append(tuple(i))
        table = MDDataTable(
            use_pagination=True,
            column_data=[
                ('stock', dp(20)),
                ('oldest_price', dp(25)),
                ('oldest_quantity', dp(35)),
                ('current_price', dp(35)),
                ('percent_change', dp(35))
            ],
            row_data=row_data
        )
        self.root.ids.dm_cash_results.clear_widgets()
        self.root.ids.dm_cash_results.add_widget(table)

    # ############################################################## stock summary

    def show_stock_summary(self):
        tickers = self.root.ids.dm_tickers.text
        data_tickers = self.df['ticker'].unique().tolist()
        if len(tickers) == 0:
            available_stocks = data_tickers
        else:
            stock_list = tickers.replace(' ', '').upper().split(',')
            available_stocks = [t for t in stock_list if t in data_tickers]
        if len(available_stocks) != 0:
            df_summary = self.df_get_summary_data(available_stocks, self.df)
            row_data = []
            for i in df_summary:
                row_data.append(tuple(i))
        else:
            row_data = [('None', 'None', 'None', 'None')]
        table = MDDataTable(
            use_pagination=True,
            column_data=[
                ('stock', dp(35)),
                ('total_units', dp(35)),
                ('min_max', dp(35)),
                ('current_price', dp(45))
            ],
            row_data=row_data
        )
        self.root.ids.dm_sum_results.clear_widgets()
        self.root.ids.dm_sum_results.add_widget(table)

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.title = 'Datatota-Prototypes AMBER'
        return AmberContent()


if __name__ == '__main__':
    AmberApp().run()










