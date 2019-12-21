import pandas as pd
import numpy as np
import sys
sys.path.append("../")
import os
sys.path.append(os.path.abspath(""))
# from preprocessing.Normalize import Normalize
from preprocessing.Normalize import Normalize
from sklearn.model_selection import KFold
import helper.Help as helper
import time

class KCrossValidation():
    
    def __init__(self,k : int = 10):
        n = Normalize()        
        norm_data = n.get_normalized_data()
        np_series = helper.series_df_to_numpy(norm_data.T)
        del n #deleting n to save mememory
        self.run_kfold(np_series,k)

    def run_kfold(self,np_series,k:int=10):
        kf = KFold(n_splits=k)
        for train, test in kf.split(np_series):
            x_train = np_series[test]
            print("train")
            print(train)
            print("test")
            print(test)

        # for train,test in 
