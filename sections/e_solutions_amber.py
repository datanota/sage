
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from functools import partial
import pandas as pd


class Amber:
    def __init__(self):
        super().__init__()

# ############################################################## Amber design

    def dict_amber(self):
        return {
            'model_type': 'stock investment recommendation',
            'layout': self.get_amber_widgets,
            'data': self.get_df_available_stocks_data,
            'buy': {
                'hint_text': 'investment dollar amount (default value is $1000)',
                'btn_text': 'buy recommendation',
                'btn_bind': self.show_investment_recommendations
            },
            'sell': {
                'hint_text': 'cash dollar amount (default value is $1000)',
                'btn_text': 'sell recommendation',
                'btn_bind': self.show_cash_recommendations
            }
        }

    def get_amber_widgets(self, tp, sage_theme_dict, assets_path, data):
        amber_layout = BoxLayout(orientation='vertical')
        default_tab = TabbedPanelItem(text='schema', color=sage_theme_dict.get('dn_gold'), background_down='')
        default_tab_layout = BoxLayout(orientation='vertical')
        default_tab_title = MDLabel(
            text='Amber: ' + self.dict_amber().get('model_type'), text_color=sage_theme_dict.get('app_text'),
            size_hint=[1, 0.2], font_style='H4', halign='center', theme_text_color='Custom'
        )
        default_tab_layout.add_widget(default_tab_title)
        default_tab_layout.add_widget(Image(source=f"{assets_path}db_schema_amber.png", allow_stretch=True))
        default_tab.add_widget(default_tab_layout)
        tp.add_widget(default_tab)
        for action in ['buy', 'sell']:
            tab = TabbedPanelItem(text=action, color=sage_theme_dict.get('dn_gold'), background_down='')
            tab_parent_layout = GridLayout(rows=2)
            top_layout = BoxLayout(orientation='horizontal', spacing='10sp', size_hint=[1, 0.15], padding=[10, 10, 10, 5])
            text_input = MDTextFieldRect(
                multiline=False, cursor_color=sage_theme_dict.get('input_box_foreground'), font_size='18sp',
                hint_text=self.dict_amber().get(action).get('hint_text'), background_normal='',
                hint_text_color=sage_theme_dict.get('input_box_hint'),
                foreground_color=sage_theme_dict.get('input_box_foreground'),
                background_color=sage_theme_dict.get('input_box_background')
            )
            given_input = text_input.text
            top_layout.add_widget(text_input)
            section_button = MDFillRoundFlatButton(
                text=self.dict_amber().get(action).get('btn_text'), font_size='20sp',
                size_hint=[0.6, 1], md_bg_color=sage_theme_dict.get('app_button_background')
            )
            tab_result_layout = BoxLayout(orientation='vertical')
            section_button.bind(
                on_press=partial(
                    self.dict_amber().get(action).get('btn_bind'), tab_result_layout, given_input, data
                )
            )
            top_layout.add_widget(section_button)
            tab_parent_layout.add_widget(top_layout)
            tab_parent_layout.add_widget(tab_result_layout)
            tab.add_widget(tab_parent_layout)
            tp.add_widget(tab)
        amber_layout.add_widget(tp)
        return amber_layout

# ############################################################## Amber dataset

    def get_df_available_stocks_data(self, data_file):
        df = self.get_df_stocks_data(data_file)
        df = df[df['sold'] == 0]
        df.insert(6, 'pq', df['unit_price'] * df['quantity'])
        return df

    @staticmethod
    def get_df_stocks_data(data_file):
        stocks_df = pd.read_excel(f'{data_file}', sheet_name=0, index_col=None)
        for str_col in ['transaction_id', 'stock_id', 'date', 'ticker']:
            stocks_df[str_col] = stocks_df[str_col].astype('string')
        for float_col in ['unit_price', 'quantity']:
            stocks_df[float_col] = stocks_df[float_col].astype('float')
        updates_df = pd.read_excel(data_file, sheet_name=1, index_col=None)
        for str_col in ['stock_id', 'ticker', 'updated_date']:
            updates_df[str_col] = updates_df[str_col].astype('string')
        df = pd.merge(stocks_df, updates_df, on=['stock_id', 'ticker'])
        return df

# ############################################################## decision helper -- buy

    def show_investment_recommendations(self, *args):
        result_widget = args[0]
        inv_dollar = args[1]
        df = args[2]
        row_data = []
        if inv_dollar == '':
            inv_dollar = 1000.0
        else:
            inv_dollar = float(inv_dollar)
        buy_list = self.get_investment_recommendations(inv_dollar, df)
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
        _ = args[1]
        df = args[2]
        row_data = []
        sell_list = self.get_cash_recommendations(df)
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
