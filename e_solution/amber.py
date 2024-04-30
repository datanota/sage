
from utilities.common import Common
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from functools import partial
import pandas as pd


class Amber(Common):
    def __init__(self):
        super().__init__()
        self.amber_dict = self.dict_amber_section()
        self.amber_data_path = f'{self.sage_solution_path}amber.xlsx'
        self.amber_df = self.get_df_available_stocks_data()

    def get_amber_section_tab(self, section):
        """
        :param section: the individual tab after default tab
        :return:
            - creates a tab, adds input bux and button widgets
            - adds a placeholder box for the results if button is pressed
        """
        tab = TabbedPanelItem(text=section, color=[215 / 255, 163 / 255, 9 / 255], background_down='')
        tab_parent_layout = GridLayout(rows=2)
        top_layout = BoxLayout(orientation='horizontal', spacing='10sp', size_hint=[1, 0.15], padding=[10, 10, 10, 5])
        text_input = MDTextFieldRect(
            multiline=False, cursor_color=[196/255, 204/255, 217/255], font_size='18sp',
            hint_text=self.amber_dict.get(section).get('hint_text'), background_normal='',
            background_color='AFA687'
        )
        given_input = text_input.text
        top_layout.add_widget(text_input)
        section_button = MDFillRoundFlatButton(
            text=self.amber_dict.get(section).get('btn_text'), font_size='20sp',
            size_hint=[0.6, 1], md_bg_color=self.amber_dict.get(section).get('background_color')
        )
        tab_result_layout = BoxLayout(orientation='vertical')
        section_button.bind(on_press=partial(self.amber_dict.get(section).get('btn_bind'), tab_result_layout, given_input))
        top_layout.add_widget(section_button)
        tab_parent_layout.add_widget(top_layout)
        tab_parent_layout.add_widget(tab_result_layout)
        tab.add_widget(tab_parent_layout)
        return tab

    def dict_amber_section(self):
        d = {
            'database': {
                'hint_text': 'stock ticker (separate by comma)',
                'btn_text': 'show stocks',
                'background_color': 'E4C772',
                'btn_bind': self.show_stock_summary
            },
            'buy': {
                'hint_text': 'investment dollar amount (default value is $1000)',
                'btn_text': 'recommend top stocks',
                'background_color': 'A9C789',
                'btn_bind': self.show_investment_recommendations
            },
            'sell': {
                'hint_text': 'cash dollar amount (default value is $1000)',
                'btn_text': 'stocks to sell',
                'background_color': 'CC8787',
                'btn_bind': self.show_cash_recommendations
            }
        }
        return d

# ############################################################## Amber dataset

    def get_df_available_stocks_data(self):
        df = self.get_df_stocks_data()
        df = df[df['sold'] == 0]
        df.insert(6, 'pq', df['unit_price'] * df['quantity'])  # unit_price times quantity
        return df

    def get_df_stocks_data(self):
        stocks_df = pd.read_excel(self.amber_data_path, sheet_name=0, index_col=None)
        for str_col in ['transaction_id', 'stock_id', 'date', 'ticker']:
            stocks_df[str_col] = stocks_df[str_col].astype('string')
        for float_col in ['unit_price', 'quantity']:
            stocks_df[float_col] = stocks_df[float_col].astype('float')
        updates_df = pd.read_excel(self.amber_data_path, sheet_name=1, index_col=None)
        for str_col in ['stock_id', 'ticker', 'updated_date']:
            updates_df[str_col] = updates_df[str_col].astype('string')
        df = pd.merge(stocks_df, updates_df, on=['stock_id', 'ticker'])
        return df

# ############################################################## decision helper -- buy

    def show_investment_recommendations(self, *args):
        result_widget = args[0]
        inv_dollar = args[1]
        row_data = []
        if inv_dollar == '':
            inv_dollar = 1000.0
        else:
            inv_dollar = float(inv_dollar)
        buy_list = self.get_investment_recommendations(inv_dollar, self.amber_df)
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
        result_widget.clear_widgets()
        result_widget.add_widget(table)
        self.amber_df = self.get_df_available_stocks_data()

    def get_investment_recommendations(self, inv_dollar, df):
        df = self.df_buy_computations(inv_dollar, df)
        df = df[['ticker', 'current_q', 'current_price', 'pr_change']].drop_duplicates()
        df = df.sort_values(by=['pr_change'], ascending=True)
        buy_list = df.values.tolist()
        return buy_list

    @staticmethod
    def df_buy_computations(inv_dollar, df):
        final_df = []
        df.insert(9, 'current_q', round(inv_dollar / df['current_price']))
        df.insert(10, 'current_pq', df['current_price'] * df['current_q'])
        tickers = df['ticker'].unique().tolist()
        for ticker in tickers:
            df1 = df[df['ticker'] == ticker]
            pq_sum = df1['pq'].sum()
            q_sum = df1['quantity'].sum()
            current_pq = df1['current_pq'].iloc[0]
            current_q = df1['current_q'].iloc[0]
            df1.insert(6, 'wa', round(pq_sum / q_sum, 2))
            df1.insert(7, 'wa_c', round((pq_sum + current_pq) / (q_sum + current_q), 2))
            wa = df1['wa'].iloc[0]
            wa_c = df1['wa_c'].iloc[0]
            df1.insert(8, 'pr_change', round(round((wa_c - wa) / wa, 4) * 100, 2))
            final_df.append(df1)
        results_df = pd.concat(final_df)
        return results_df

# ############################################################## decision helper -- sell

    def show_cash_recommendations(self, *args):
        result_widget = args[0]
        row_data = []
        sell_list = self.get_cash_recommendations(self.amber_df)
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
        result_widget.clear_widgets()
        result_widget.add_widget(table)

    def get_cash_recommendations(self, df):
        df = self.df_sell_computations(df)
        df = df[['ticker', 'oldest_price', 'oldest_q', 'current_price', 'pr_change']].drop_duplicates()
        df = df.sort_values(by=['pr_change'], ascending=True)
        sell_list = df.values.tolist()
        return sell_list

    @staticmethod
    def df_sell_computations(df):
        final_df = []
        tickers = df['ticker'].unique().tolist()
        for ticker in tickers:
            df1 = df[df['ticker'] == ticker]
            df1 = df1.sort_values(by=['date'], ascending=True)
            oldest_date= df1['date'].iloc[0]
            oldest_price = df1['unit_price'].iloc[0]
            df1.insert(6, 'oldest_price', oldest_price)
            oldest_q = df1['quantity'].iloc[0]
            df1.insert(7, 'oldest_q', oldest_q)
            pq_sum1 = df1['pq'].sum()
            q_sum1 = df1['quantity'].sum()
            wa1 = round(pq_sum1 / q_sum1, 2)
            df1.insert(8, 'wa1', wa1)
            df2 = df1[df1['date'] != oldest_date]
            if len(df2) != 0:
                pq_sum2 = df2['pq'].sum()
                q_sum2 = df2['quantity'].sum()
                wa2 = round(pq_sum2 / q_sum2, 2)
                df1.insert(9, 'wa2', wa2)
                pr_change = round(round((wa2 - wa1) / wa1, 4) * 100, 2)
                df1.insert(10, 'pr_change', pr_change)
            else:
                df1.insert(10, 'pr_change', 0)
            final_df.append(df1)
        results_df = pd.concat(final_df)
        return results_df

# ############################################################## stock summary

    def show_stock_summary(self, *args):
        result_widget = args[0]
        tickers = args[1]
        data_tickers = self.amber_df['ticker'].unique().tolist()
        if len(tickers) == 0:
            available_stocks = data_tickers
        else:
            stock_list = tickers.replace(' ', '').upper().split(',')
            available_stocks = [t for t in stock_list if t in data_tickers]
        if len(available_stocks) != 0:
            df_summary = self.df_get_summary_data(available_stocks, self.amber_df)
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
        result_widget.clear_widgets()
        result_widget.add_widget(table)

    @staticmethod
    def df_get_summary_data(stock_list, df):
        table_data = []
        for ticker in stock_list:
            t = df[df['ticker'] == ticker]
            total = t['quantity'].sum()
            min_max = str(t['unit_price'].min()) + '-' + str(t['unit_price'].max())
            current_price = t['current_price'].iloc[0]
            ticker_results = [ticker, total, min_max, current_price]
            table_data.append(ticker_results)
        return table_data
