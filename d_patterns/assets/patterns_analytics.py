
from utilities.common import Common
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib
import random
matplotlib.use('Agg')


class PattersAnalytics(Common):
    """
    to create graphs and stats for patterns
    """
    def __init__(self):
        super().__init__()

    def run(self):
        print(self.app_nm)
        n_n = pd.read_csv('./assets/num_vs_num.csv')
        print(n_n.head().to_string())
        n_c = pd.read_csv('./assets/num_vs_cat.csv')
        print(n_c.head().to_string())
        c_c = pd.read_csv('./assets/cat_vs_cat.csv')
        print(c_c.head().to_string())
        print('============ DONE ============')

# ######################################################## Categorical vs. Categorical

    def cat_vs_cat(self):
        print('===== cat vs. cat')
        prd_id = list(range(1, 101))
        df = pd.DataFrame(prd_id, columns=['id'])
        np.random.seed(0)
        df['gender'] = random.choices(['Male', 'Female'], k=100)
        sample_num = random.sample(list(df['id']), 30)
        df['product'] = np.where(df['id'].isin(sample_num), 'A', 'B')
        print(df.to_string())
        # df.to_csv('./cat_vs_cat.csv', index=False)
        self.visual_stacked_bar_plot(
            df=df, cat1='gender', cat2='product',
            title='Product per Gender',
            save_path='./', fig_nm='cat_vs_cat.png'
        )

    @staticmethod
    def visual_stacked_bar_plot(df, cat1, cat2, title, save_path, fig_nm):
        sns.set(style="darkgrid")
        plt.figure(figsize=(10, 5))
        df.groupby([cat1, cat2]).size().unstack(fill_value=0).plot(
            kind='bar', stacked=True, color=['#FDBA74', '#7AB6D6']
        )
        plt.xticks(rotation=45)
        plt.title(title)
        plt.legend(loc='upper left', title='')
        plt.savefig(save_path + fig_nm, bbox_inches='tight')

# ######################################################## Numeric vs. Categorical

    def num_vs_cat(self):
        print('===== num vs. cat')
        prd_id = list(range(1, 101))
        df = pd.DataFrame(prd_id)
        np.random.seed(0)
        df['sales'] = np.random.normal(0, 1, 100) + random.sample(range(1000), 100)
        sample_num = random.sample(list(df['sales']), 30)
        df['product'] = np.where(df['sales'].isin(sample_num), 'A', 'B')
        print(df.to_string())
        # df.to_csv('./num_vs_cat.csv', index=False)
        self.visual_box_plot(
            df=df, cat_col='product', num_col='sales',
            title='Sales Dollar Amount per Product',
            save_path='./', fig_nm='num_vs_cat.png'
        )

    @staticmethod
    def visual_box_plot(df, cat_col, num_col, title, save_path, fig_nm):
        sns.set_theme(style='darkgrid')
        plt.figure(figsize=(8, 5))
        sns.boxplot(x=cat_col, y=num_col, data=df)
        plt.title(title, fontsize=20)
        plt.savefig(save_path + fig_nm, bbox_inches='tight')
        plt.close()

# ######################################################## Numeric vs. Numeric

    def num_vs_num(self):
        print('===== num vs. num')
        prd_id = list(range(1, 101))
        df = pd.DataFrame(prd_id)
        np.random.seed(0)
        noise_data = np.random.normal(0, 1, 100)
        df['quantity'] = np.random.normal(0, 1, 100)
        df['unit_price'] = abs((0.8 * df['quantity']) + (np.sqrt(1 - 0.8 ** 2) * noise_data))
        df['quantity'] = df['quantity'] + random.sample(range(1000), 100)
        print(df.to_string())
        # df.to_csv('./num_vs_num.csv', index=False)
        self.visual_scatter_plot(
            df=df, x='quantity', y='unit_price',
            title='Quantity vs. Unit Price',
            save_path='./', fig_nm='num_vs_num.png'
        )

    @staticmethod
    def visual_scatter_plot(df, x, y, title, save_path, fig_nm):
        sns.set_theme(style='darkgrid')
        plt.figure(figsize=(8, 5))
        sns.scatterplot(data=df, x=x, y=y, c='#7AB6D6', s=200, alpha=0.7, palette='viridis')
        plt.title(title)
        plt.savefig(save_path + fig_nm, bbox_inches='tight')


if __name__ == '__main__':
    PattersAnalytics().run()

