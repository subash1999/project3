import pandas as pd
import numpy as np
import sys
sys.path.append('../')
import os
sys.path.append(os.path.abspath(""))
class GetData():
    def __init__(self):
        self._data_summary = "data_summary.csv"
        self._df_data_summary = pd.read_csv(self._data_summary)
        self.available_types = ["clinical","series_matrix"]
        pass

    def get_path(self,data_name : str,type_ :str ):
        temp_df = self._get_filtered_df(data_name,type_)
        return str(temp_df.iloc[0]["path"])

    def get_file_name(self,data_name : str,type_ :str ):
        temp_df = self._get_filtered_df(data_name,type_)
        return str(temp_df.iloc[0]["file_name"])

    def get_file_name_with_path(self,data_name : str,type_ :str ):
        temp_df = self._get_filtered_df(data_name,type_)
        return str(temp_df.iloc[0]["file_name_with_path"])

    def _get_filtered_df(self,data_name : str,type_ :str ):
        if(self._check_type(type_)):
            temp_df = self._df_data_summary[self._df_data_summary["name"] == data_name]
            temp_df = temp_df[temp_df["type"] == type_]
            return temp_df
        else : 
            sys.exit(0)
    def _check_type(self,type_ : str)-> bool:
        if type_ in self.available_types : 
            return True
        else : 
            print("Type must be one of : ",str(self.available_types))
            return False
