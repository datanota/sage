
from utilities.common import Common
import pandas as pd
import sqlite3


class CreateDatabase(Common):
    def __init__(self):
        super().__init__()

    def df_to_db(self):
        self.create_shopping_db_table()
        self.populate_shopping_db_tables()

    def populate_shopping_db_tables(self):
        db_conn = sqlite3.connect(f'{self.db_path}shopping.db')

        customers = pd.read_csv(f'{self.generated_data_path}customers.csv')
        customers.to_sql(name='customers', con=db_conn, if_exists='replace', index=False)

        products = pd.read_csv(f'{self.generated_data_path}products.csv')
        products.to_sql(name='products', con=db_conn, if_exists='replace', index=False)

        orders = pd.read_csv(f'{self.generated_data_path}orders.csv')
        orders.to_sql(name='orders', con=db_conn, if_exists='replace', index=False)

        db_conn.commit()
        db_conn.close()

    def create_shopping_db_table(self):
        db_conn = sqlite3.connect(f'{self.db_path}shopping.db')
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
                customer_id INTEGER PRIMARY KEY, 
                full_nm STRING, 
                age INTEGER,
                location text
                );
             """
        return table

    @staticmethod
    def create_products_table():
        table = """
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY,  
                name STRING,
                category STRING,
                unit_price INTEGER
                );
             """
        return table

    @staticmethod
    def create_orders_table():
        table = """
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER,
                product_id INTEGER PRIMARY KEY, 
                customer_id INTEGER, 
                quantity INTEGER,
                date datetime
                );
             """
        return table

