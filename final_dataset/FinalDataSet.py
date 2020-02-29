import pandas as pd
import numpy as np
import sys
import concurrent.futures
import gc
import os
sys.path.append(os.path.abspath(""))
sys.path.append(os.path.abspath("../"))

import helper.SeriesHelper as series_helper
# from h.series_helper import get_relapse_value_from_series_matrix

class FinalDataSet():
    def __init__(self):
        self._series_helper = series_helper
        self._series_files = [
            "final_dataset/combined_matrix_final_1.csv",
            "final_dataset/combined_matrix_final_2.csv",
            "final_dataset/combined_matrix_final_3.csv",
            "final_dataset/combined_matrix_final_4.csv",
            "final_dataset/combined_matrix_final_5.csv",
        ]
        self._clinical_file = "final_dataset/combined_clinical_final.csv"
        self.make_series_matrix()
        # self.thread_make_series_matrix()
        self.make_clinical()
        self._relapse_array = self._series_helper.get_relapse_value_from_series_matrix(self._series_matrix.copy())

    def thread_make_series_matrix(self):
        df_list = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_url = {executor.submit(pd.read_csv, fn): fn for fn in self._series_files}
            for future in concurrent.futures.as_completed(future_to_url):
                df_list.append(future.result())
        self._series_matrix = pd.concat(df_list,ignore_index=True)[:]
        cols = list(self._series_matrix.columns)
        cols[0] = "GEO_ACC"
        self._series_matrix.columns = cols
        self._series_matrix = self._series_matrix.set_index("GEO_ACC").T
        gc.collect()
        return self._series_matrix

    def make_series_matrix(self):
        df_list = []
        for file_name in self._series_files:
            df_list.append(pd.read_csv(file_name))
        self._series_matrix = pd.concat(df_list,ignore_index=True)[:]
        cols = list(self._series_matrix.columns)
        cols[0] = "GEO_ACC"
        self._series_matrix.columns = cols
        self._series_matrix = self._series_matrix.set_index("GEO_ACC").T
        gc.collect()       
        return self._series_matrix

    def get_train_test_data(self):
        X_train = pd.read_csv("final_dataset/X_train.csv")
        X_test = pd.read_csv("final_dataset/X_test.csv")
        y_train = pd.read_csv("final_dataset/y_train.csv")
        y_test = pd.read_csv("final_dataset/y_test.csv")
        return X_train,X_test,y_train,y_test
    
    def make_clinical(self):
        self._clinical  = pd.read_csv(self._clinical_file)
        return self.clinical
    
    def get_relapse_value(self,id_ref : str):
        self._series_helper.get_relapse_value(id_ref)

    @property
    def series_matrix(self):
        return self._series_matrix
    
    @property
    def clinical(self):
        return self._clinical
    
    @property
    def series_matrix_array(self):
        return self.series_matrix.to_numpy()
    
    @property
    def sample_list(self):
        return list(self.series_matrix.index)
    
    @property
    def id_ref(self):
        return list(self.series_matrix.columns)

    @property
    def relapse_array(self):
        return self._relapse_array

