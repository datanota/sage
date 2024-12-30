
from kivymd.uix.textfield import MDTextFieldRect
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivy.uix.image import Image
from functools import partial
from faker import Faker
import pandas as pd
import numpy as np
import random
import string
import uuid
import time


class Dataset:
    def __init__(self):
        self.cust_num = 0
        self.prd_num = 0
        self.order_num = 0

    @staticmethod
    def get_dataset_attributes_tabs(sage_theme_dict, data_name, section, img_source):
        tab = TabbedPanelItem(
            text=section, color=sage_theme_dict.get('dn_gold'), background_down=''
        )
        parent_widget = BoxLayout(orientation='vertical', spacing='10sp')
        if section == 'activity':
            s_label = MDLabel(
                text=f'{data_name} {section}', halign='center', theme_text_color='Custom',
                text_color=sage_theme_dict.get('app_text'), font_style='H4', size_hint=[1, 0.1]
            )
            parent_widget.add_widget(s_label)
        s_img = Image(source=img_source, allow_stretch=True)
        parent_widget.add_widget(s_img)
        tab.add_widget(parent_widget)
        return tab

    def get_generate_dataset_widgets(self, sage_theme_dict, db_schema_path, data_name, generated_data_path):
        gen_tab = TabbedPanelItem(text='generate', color=sage_theme_dict.get('dn_gold'), background_down='')
        gen_parent_widget = BoxLayout(orientation='vertical')
        gen_top_widget = GridLayout(rows=1, size_hint=[1, 0.13], padding='5sp')
        gen_bottom_widget = BoxLayout(orientation='vertical', size_hint=[1, 0.75], padding=[0, 50, 0, 0])
        gen_info_widget = BoxLayout(orientation='vertical', size_hint=[1, 0.12])
        row_input = MDTextFieldRect(
            multiline=False, cursor_color=sage_theme_dict.get('input_box_foreground'), font_size='18sp',
            background_normal='', hint_text='how many rows of data? (default limits: 20 - 2000)',
            hint_text_color=sage_theme_dict.get('input_box_hint'),
            foreground_color=sage_theme_dict.get('input_box_foreground'),
            background_color=sage_theme_dict.get('input_box_background')
        )
        gen_top_widget.add_widget(row_input)
        gen_button = Button(
            text='generate data', color=sage_theme_dict.get('app_button_text'), size_hint=[0.3, 1], font_size='18sp', background_normal='',
            background_color=sage_theme_dict.get('app_button_background')
        )
        gen_button.bind(
            on_release=partial(
                self.df_to_file_save_generated_data,
                row_input, gen_info_widget, data_name, generated_data_path, sage_theme_dict
            )
        )
        gen_top_widget.add_widget(gen_button)
        gen_parent_widget.add_widget(gen_top_widget)
        gen_schema = Image(source=db_schema_path, allow_stretch=True)
        gen_bottom_widget.add_widget(gen_schema)
        gen_parent_widget.add_widget(gen_bottom_widget)
        gen_parent_widget.add_widget(gen_info_widget)
        gen_tab.add_widget(gen_parent_widget)
        return gen_tab

    def df_to_file_save_generated_data(self, *args):
        """
        :param args: args[0] is the given data size with default data size limits of 20 - 2000 rows
        """
        given_data_size = int(args[0].text) if args[0].text.strip() != '' else 20
        gen_info_widget = args[1]
        data_name = args[2]
        generated_data_path = args[3]
        sage_theme_dict = args[4]
        try:
            sage_dataset_size = given_data_size if (given_data_size >= 20 or given_data_size <= 2000) else 20
        except ValueError:
            print('setting default data size of 20')
            sage_dataset_size = 20
        df = self.generate_shopping_data(sage_dataset_size, generated_data_path)
        lb_info = MDLabel(
            text=f"{data_name} dataset size: {print(df) if df is None else df.shape}\n"
                 f"data files are saved in directory: {generated_data_path.split('sage')[1]}",
            text_color=sage_theme_dict.get('app_text'), font_style='H6', padding='30sp'
        )
        gen_info_widget.clear_widgets()
        gen_info_widget.add_widget(lb_info)

    def generate_shopping_data(self, sage_dataset_size, generated_data_path):
        cust_file = f'{generated_data_path}customers.csv'
        self.cust_num = round(sage_dataset_size/2)
        cust = self.df_customers_data()

        prd_file = f'{generated_data_path}products.csv'
        self.prd_num = round(sage_dataset_size / 4)
        prd = self.df_products_data()

        order_file = f'{generated_data_path}orders.csv'
        order = self.df_orders_data(sage_dataset_size=sage_dataset_size, all_customers=list(cust['customer_id']), all_products=list(prd['product_id']))

        shopping_file = f'{generated_data_path}shopping.csv'
        shopping_df = order.merge(cust, on='customer_id').merge(prd, on='product_id')

        cust.to_csv(cust_file, index=False)
        print(' =========== customers file is saved =========== ')
        prd.to_csv(prd_file, index=False)
        print(' =========== products file is saved =========== ')
        order.to_csv(order_file, index=False)
        print(' =========== orders file is saved =========== ')
        shopping_df.to_csv(shopping_file, index=False)
        print(' =========== shopping file is saved =========== ')
        time.sleep(1)
        return shopping_df

# ################################################################
# ################################################################ customers
# ################################################################

    def df_customers_data(self):
        data = {
            'customer_id': [], 'full_nm': [], 'age': [],
            'location': [], 'loyalty_points': [], 'gender': []
        }
        for _ in range(self.cust_num):
            data['customer_id'].append(uuid.uuid4())
            data['full_nm'].append(Faker().name())
            data['age'].append(random.choice(list(np.arange(15, 91))))
            data['location'].append(random.choice([
                'Paris, France', 'Milan, Italy', 'LA, California, USA', 'Madrid, Spain', 'San Jose, California, USA',
                'Rio de Janeiro, Brazil', 'KL, Malaysia', 'Salt Lake City, Utah, USA', 'Portland, Oregon, USA'
            ]))
            data['loyalty_points'].append(random.randint(1, 100))
            data['gender'].append(random.choice(['male', 'female', 'other']))
        df = pd.DataFrame(data)
        df['last_login_date'] = self.sage_generate_date_column(start='2020-01-01', end='2024-03-30', total_num=self.cust_num)
        return df

# ################################################################
# ################################################################ products
# ################################################################

    def df_products_data(self):
        letters = list(string.ascii_lowercase)
        data = {
            'product_id': [], 'prd_name': [], 'prd_category': [],
            'unit_price': [], 'prd_description': []
        }
        for _ in range(self.prd_num):
            data['product_id'].append(uuid.uuid4())
            data['prd_name'].append(''.join(random.sample(letters, 4)))
            data['prd_category'].append(random.choice(['electronics', 'apparel', 'beauty', 'home']))
            data['prd_description'].append(Faker().text(max_nb_chars=50))
            data['unit_price'].append(round(random.choice(list(np.arange(0, 100, 0.1))), 2))
        df = pd.DataFrame(data)
        return df

# ################################################################
# ################################################################ orders
# ################################################################

    def df_orders_data(self, sage_dataset_size, all_customers, all_products):
        data = {
            'order_id': [], 'customer_id': [], 'product_id': [],
            'order_quantity': [], 'purchased_via': [], 'order_delivered': [],
            'order_returned': []
        }
        for _ in range(sage_dataset_size):
            data['order_id'].append(uuid.uuid4())
            data['customer_id'].append(random.choice(all_customers))
            data['product_id'].append(random.choice(all_products))
            data['order_quantity'].append(random.choice(list(range(0, 1000))))
            data['purchased_via'].append(random.choice(['amazon', 'website', 'in-store']))
            data['order_delivered'].append(random.choice(['yes', 'no']))
            data['order_returned'].append(random.choice([True, False]))
        df = pd.DataFrame(data)
        df['order_date'] = self.sage_generate_date_column(start='2021-01-01', end='2023-12-30', total_num=sage_dataset_size)
        return df

    @staticmethod
    def sage_generate_date_column(start, end, total_num):
        x = np.random.randint(pd.Timestamp(start).value, pd.Timestamp(end).value, total_num)
        dates = [pd.to_datetime(i).strftime('%Y-%m-%d') for i in x]
        return dates
