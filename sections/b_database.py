
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivy.uix.image import Image
import pandas as pd
import sqlite3


class Database:
    def __init__(self):
        pass

    @staticmethod
    def db_widgets(sage_theme_dict, img_source):
        btn = Button(
            text=f'create shopping database', color=[0, 0, 0], font_size='20sp',
            size_hint=[0.5, 0.15], pos_hint={'center_x': 0.5, 'center_y': 0.5},
            background_normal='', background_color=sage_theme_dict.get('app_button_background')
        )
        img = Image(source=img_source, allow_stretch=True)
        info_widget = BoxLayout(orientation='vertical', size_hint=[1, 0.1])
        return btn, img, info_widget

    def create_db(self, *args):
        shopping_db_path = args[0]
        generated_data_path = args[1]
        info_widget = args[2]
        try:
            self.df_to_sqlite_db(shopping_db_path, generated_data_path)
            lbd = MDLabel(
                text=f"database is created in directory: {shopping_db_path.split('sage')[1]}",
                font_style='H5', halign='center', padding=[100, 0, 0, 20]
            )
        except Exception as e:
            print(e)
            lbd = MDLabel(text=f"error while creating shopping database", font_style='H5', halign='center')
        info_widget.add_widget(lbd)

    def df_to_sqlite_db(self, shopping_db_path, generated_data_path):
        self.sqlite_create_shopping_db_tables(shopping_db_path)
        self.sqlite_populate_shopping_db_tables(shopping_db_path, generated_data_path)

    def sqlite_create_shopping_db_tables(self, shopping_db_path):
        db_conn = sqlite3.connect(shopping_db_path)
        c = db_conn.cursor()
        c.execute(self.create_customers_table())
        c.execute(self.create_products_table())
        c.execute(self.create_orders_table())
        db_conn.commit()
        db_conn.close()

    @staticmethod
    def create_customers_table():
        table = """
            CREATE TABLE IF NOT EXISTS customers (
                customer_id TEXT PRIMARY KEY, 
                full_nm TEXT, 
                age INTEGER,
                location TEXT,
                loyalty_points INTEGER,
                gender TEXT,
                last_login_date datetime
                );
             """
        return table

    @staticmethod
    def create_products_table():
        table = """
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,  
                prd_name TEXT,
                prd_category TEXT,
                unit_price DECIMAL(19, 4),
                prd_description TEXT
                );
             """
        return table

    @staticmethod
    def create_orders_table():
        table = """
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                product_id TEXT, 
                customer_id TEXT, 
                order_quantity INTEGER,
                purchased_via TEXT,
                order_delivered TEXT, 
                order_returned BOOLEAN, 
                order_date datetime
                );
             """
        return table

    @staticmethod
    def sqlite_populate_shopping_db_tables(shopping_db_path, generated_data_path):
        db_conn = sqlite3.connect(shopping_db_path)

        customers = pd.read_csv(f'{generated_data_path}customers.csv')
        customers.to_sql(name='customers', con=db_conn, if_exists='replace', index=False)

        products = pd.read_csv(f'{generated_data_path}products.csv')
        products.to_sql(name='products', con=db_conn, if_exists='replace', index=False)

        orders = pd.read_csv(f'{generated_data_path}orders.csv')
        orders.to_sql(name='orders', con=db_conn, if_exists='replace', index=False)

        db_conn.commit()
        db_conn.close()
