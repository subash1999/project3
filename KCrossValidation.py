import pandas as pd
import numpy as np
import sys
sys.path.append("../")
import os
sys.path.append(os.path.abspath(""))
# from preprocessing.Normalize import Normalize
from preprocessing.Normalize import Normalize
from sklearn.model_selection import KFold
import helper.SeriesHelper as series_helper
import time

class KCrossValidation():
    
    def __init__(self,k : int = 10):
        pass
        
    
    def ge_data(self):
        n = Normalize()
        self.np_series = n.get_normalized_data().to_numpy()
        del n #deleting n to save mememory

    def run_kfold(self,np_series,k:int=10):
        kf = KFold(n_splits=k)
        tr = []
        te = []
        for train, test in kf.split(np_series):
            tr.append(train)
            te.append(test)
        return tr,te

