
from utilities.common import Common
import pandas as pd
import numpy as np
import datetime
import time
import random
import os


class DataGeneration(Common):
    def __init__(self):
        super(DataGeneration, self).__init__()

    def generate_data(self, cust_num, prd_num):
        cust_num = int(cust_num)
        prd_num = int(prd_num)

        cust_file = f'{self.data_files_path}customers.csv'
        cust = self.get_customers_data(cust_num)

        prd_file = f'{self.data_files_path}products.csv'
        prd = self.get_products_data(prd_num=prd_num)

        order_file = f'{self.data_files_path}orders.csv'
        order = self.get_orders_data(total_customers=list(cust['customer_id']), total_products=list(prd['product_id']))

        cust.to_csv(cust_file, index=False)
        print(' =========== customers file is done =========== ')
        prd.to_csv(prd_file, index=False)
        print(' =========== products file is done =========== ')
        order.to_csv(order_file, index=False)
        print(' =========== orders file is done =========== ')

        time.sleep(1)

    def get_orders_data(self, total_customers, total_products):
        order_num = round(len(total_customers)/2)
        id = self.sage_data_order_id(order_num)
        df = pd.DataFrame(id, columns=['order_id'])
        df['customer_id'] = [random.choice(total_customers) for x in range(len(df))]
        df['product_id'] = [random.choice(total_products) for x in range(len(df))]
        df['quantity'] = self.sage_data_order_quantity(order_num)
        df['date'] = self.sage_data_order_date(order_num)
        return df

    def get_products_data(self, prd_num):
        id = self.sage_data_products_id(prd_num)
        df = pd.DataFrame(id, columns=['product_id'])
        df['name'] = self.sage_data_products_name(prd_num)
        df['category'] = self.sage_data_products_category(prd_num)
        df['unit_price'] = self.sage_data_products_unit_price(prd_num)
        return df

    def get_customers_data(self, cust_num):
        id = self.sage_data_customers_id(cust_num)
        df = pd.DataFrame(id, columns=['customer_id'])
        df['full_nm'] = self.sage_data_customers_name(cust_num)
        df['age'] = self.sage_data_customers_age(cust_num)
        df['location'] = self.sage_data_customers_city_country(cust_num)
        return df

# ################################################################
# ################################################################ customers
# ################################################################

    def sage_data_customers_id(self, cust_num):
        customer_id = []
        for num in range(int(cust_num)):
            l1 = ''.join(random.sample(self.letters, 3))
            n1 = ''.join((str(n) for n in random.sample(self.numbers, 3)))
            l2 = ''.join(random.sample(self.letters, 2))
            n2 = ''.join((str(n) for n in random.sample(self.numbers, 2)))
            c_id = f'{l1}-{n1}-{l2}{n2}'
            customer_id.append(c_id)
        return customer_id

    def sage_data_customers_name(self, cust_num):
        name = []
        for num in range(cust_num):
            fn = ''.join(random.sample(self.letters, 3))
            ln = ''.join(random.sample(self.prefix, 1) + random.sample(self.letters, 4))
            full_nm = f'{fn} {ln}'
            name.append(full_nm)
        return name

    def sage_data_customers_age(self, cust_num):
        age = []
        for num in range(cust_num):
            a = random.choice(self.age_group)
            age.append(a)
        return age

    def sage_data_customers_city_country(self, cust_num):
        city_country = []
        for location in range(cust_num):
            cc = random.choice(self.location_list)
            city_country.append(cc)
        return city_country

# ################################################################
# ################################################################ products
# ################################################################

    def sage_data_products_id(self, prd_num):
        product_id = []
        for num in range(int(prd_num)):
            l1 = ''.join(random.sample(self.letters, 4))
            n1 = ''.join((str(n) for n in random.sample(self.numbers, 3)))
            c_id = f'{l1}-{n1}'
            product_id.append(c_id)
        return product_id

    def sage_data_products_name(self, prd_num):
        prd_name = []
        for num in range(prd_num):
            name = ''.join(random.sample(self.letters, 4))
            prd_name.append(name)
        return prd_name

    def sage_data_products_category(self, prd_num):
        category_name = []
        if prd_num == 0:
            category_num = 0
        elif prd_num == 1:
            category_num = 1
        else:
            category_num = round(prd_num/3)
        for num in range(category_num):
            name = ''.join(random.sample(self.letters, 5))
            category_name.append(name)
        category = random.choices(category_name, k=prd_num)
        return category

    def sage_data_products_unit_price(self, prd_num):
        unit_price = []
        for num in range(prd_num):
            p = random.choice(self.price)
            unit_price.append(round(p, 2))
        return unit_price

# ################################################################
# ################################################################ orders
# ################################################################

    def sage_data_order_id(self, order_num):
        order_id = []
        for num in range(order_num):
            a = ''.join(random.sample(self.letters, 4))
            n = ''.join((str(n) for n in random.sample(self.numbers, 3)))
            b = ''.join(random.sample(self.letters, 2))
            o_id = f'{a}-{n}-{b}'
            order_id.append(o_id)
        return order_id

    def sage_data_order_quantity(self, order_num):
        quantity = []
        for num in range(order_num):
            q = random.choice(self.quantity)
            quantity.append(q)
        return quantity

    def sage_data_order_date(self, order_num):
        x = np.random.randint(pd.Timestamp(self.start).value, pd.Timestamp(self.end).value, order_num)
        dates = [pd.to_datetime(i).strftime('%Y-%m-%d') for i in x]
        return dates



