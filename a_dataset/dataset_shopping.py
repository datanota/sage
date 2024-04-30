
from utilities.common import Common
from faker import Faker
import pandas as pd
import numpy as np
import uuid
import time
import random


class ShoppingData(Common):
    def __init__(self):
        super().__init__()
        self.cust_num = 0
        self.prd_num = 0
        self.order_num = 0

    def generate_shopping_data(self):
        cust_file = f'{self.generated_data_path}customers.csv'
        self.cust_num = round(self.sage_dataset_size/2)
        cust = self.df_customers_data()

        prd_file = f'{self.generated_data_path}products.csv'
        self.prd_num = round(self.sage_dataset_size / 4)
        prd = self.df_products_data()

        order_file = f'{self.generated_data_path}orders.csv'
        order = self.df_orders_data(all_customers=list(cust['customer_id']), all_products=list(prd['product_id']))

        shopping_file = f'{self.generated_data_path}shopping.csv'
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
        data = {
            'product_id': [], 'prd_name': [], 'prd_category': [],
            'unit_price': [], 'prd_description': []
        }
        for _ in range(self.prd_num):
            data['product_id'].append(uuid.uuid4())
            data['prd_name'].append(''.join(random.sample(self.letters, 4)))
            data['prd_category'].append(random.choice(['electronics', 'apparel', 'beauty', 'home']))
            data['prd_description'].append(Faker().text(max_nb_chars=50))
            data['unit_price'].append(round(random.choice(list(np.arange(0, 100, 0.1))), 2))
        df = pd.DataFrame(data)
        return df

# ################################################################
# ################################################################ orders
# ################################################################

    def df_orders_data(self, all_customers, all_products):
        data = {
            'order_id': [], 'customer_id': [], 'product_id': [],
            'order_quantity': [], 'purchased_via': [], 'order_delivered': [],
            'order_returned': []
        }
        for _ in range(self.sage_dataset_size):
            data['order_id'].append(uuid.uuid4())
            data['customer_id'].append(random.choice(all_customers))
            data['product_id'].append(random.choice(all_products))
            data['order_quantity'].append(random.choice(list(range(0, 1000))))
            data['purchased_via'].append(random.choice(['amazon', 'website', 'in-store']))
            data['order_delivered'].append(random.choice(['yes', 'no']))
            data['order_returned'].append(random.choice([True, False]))
        df = pd.DataFrame(data)
        df['order_date'] = self.sage_generate_date_column(start='2021-01-01', end='2023-12-30', total_num=self.sage_dataset_size)
        return df

    @staticmethod
    def sage_generate_date_column(start, end, total_num):
        x = np.random.randint(pd.Timestamp(start).value, pd.Timestamp(end).value, total_num)
        dates = [pd.to_datetime(i).strftime('%Y-%m-%d') for i in x]
        return dates

