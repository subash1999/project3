import pandas as pd
import numpy as np
import sys
sys.path.append("../")
from preprocessing.Normalize import Normalize
from sklearn.model_selection import KFold


class KCrossValidation():
    
    def __init__(self,k : int = 10):
        n = Normalize()
        norm_data = n.get_normalized_data()
        import helper.SeriesMatrix as sm
        sm.series_df_to_numpy(n.get_normalized_data())
        del n #deleting n to save mememory
    
    def run_kfold(self,k:int=0):
        kf = KFold(n_splits=k)
        # for train,test in 

k = KCrossValidation()