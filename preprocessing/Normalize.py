from scipy import stats
import numpy as np
import pandas as pd
import sys
sys.path.append('../')
import os
sys.path.append(os.path.abspath(""))
from final_dataset.FinalDataSet import FinalDataSet
from sklearn import preprocessing


class Normalize():
    def __init__(self):
        pass
    
    def get_normalized_data(self):
        f = FinalDataSet()
        series = f.series_matrix
        # print(series.head())
        x = series.values #returns a numpy array
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        series = pd.DataFrame(x_scaled,index=series.index,columns=series.columns)
        # print(series.head())
        del f
        return series
