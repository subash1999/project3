import pandas as pd
import numpy as np
import sys
import concurrent.futures
import gc
sys.path.append('../')
import os
sys.path.append(os.path.abspath(""))

class FinalDataSet():
    def __init__(self):
        self._series_files = [
            "final_dataset/combined_matrix_final_1.csv",
            "final_dataset/combined_matrix_final_2.csv",
            "final_dataset/combined_matrix_final_3.csv",
            "final_dataset/combined_matrix_final_4.csv",
            "final_dataset/combined_matrix_final_5.csv",
        ]
        self._clinical_file = "final_dataset/combined_clinical_final.csv"
        # self.make_series_matrix()
        self.thread_make_series_matrix()
        self.make_clinical()

        
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
    
    def make_clinical(self):
        self._clinical  = pd.read_csv(self._clinical_file)
        return self.clinical
    
    def get_relapse_value(self,id_ref : str):
        df = self._clinical[self._clinical.ID == id_ref]
        if df.shape[0] >1 :
            print("There are %d relapse value for same ID in clinical data,Please Check",
            df.shape[0])
            sys.exit(0)
        elif df.shape[0] < 1:
            print("No values present for relapse in the given clinical data")
            # sys.exit(0)
        else : 
            return int(df.iloc[0]["relapse"])

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
f = FinalDataSet()
print(f.series_matrix_array)
