
import numpy as np
import os
import string


class Common:
    def __init__(self):
        self.app_nm = 'SAGE'
        self.project_path = os.getcwd().split('sage')[0]
        self.data_path = 'sage/data/'
        self.data_files = 'data_files/'
        self.data_files_path = self.project_path + self.data_path + self.data_files
        self.q_files = 'query_results_files/'
        self.q_files_path = self.project_path + self.data_path + self.q_files

        self.numbers = list(np.arange(10))
        self.age_group = list(np.arange(15, 91))
        self.letters = list(string.ascii_lowercase)
        self.prefix = ['Mc', 'Ash', 'Ban', 'Fitz', 'De', 'Nin', 'El']
        self.location_list = ['Paris, France', 'Milan, Italy', 'LA, USA', 'Madrid, Spain', 'San Jose, USA']
        self.price = list(np.arange(0, 100, 0.1))
        self.quantity = list(range(0, 1000))
        self.start = '2022-01-01'
        self.end = '2023-12-30'



