from scipy import stats
import numpy as np
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath("../"))
sys.path.append(os.path.abspath(""))
from final_dataset.FinalDataSet import FinalDataSet
from sklearn import preprocessing
import pickle


class Normalize():
    def __init__(self):
        pass

    def add_pickle(self,object,filename):
        with open(filename+'.pickle', 'wb') as f:
            pickle.dump(object, f)

    def load_pickle(self,filename):
    #     print(filename)
        with open(filename+'.pickle','rb') as f:
            return pickle.load(f)

    
    
    def get_normalized_data(self):
        f = FinalDataSet()
        series = f.series_matrix
        
        # Scaling the series
        x = series.values #returns a numpy array
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        series = pd.DataFrame(x_scaled,index=series.index,columns=series.columns)

        # Removing the highly correlated columns i.e >0.8
        remove_list = list(set(self.load_pickle("final_dataset/to_remove")))
        remove_list = series.columns[remove_list]
        del f
        return series.drop(columns=list(remove_list))
    
    def get_train_test(self):
        f = FinalDataSet()
        X_train,X_test,y_train,y_test = f.get_train_test_data()
        
        train_shape = X_train.shape
        test_shape = X_test.shape

        series = pd.concat([X_train,X_test])
        
        # Scaling the series
        x = series.values #returns a numpy array
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        series = pd.DataFrame(x_scaled,index=series.index,columns=series.columns)

        # Removing the highly correlated columns i.e >0.8
        remove_list = list(set(self.load_pickle("final_dataset/to_remove")))
        remove_list = series.columns[remove_list]
        del f
        series =  series.drop(columns=list(remove_list))
        X_train = series[:train_shape[0]]
        X_test = series[train_shape[0]:]
        y_train = y_train.values
        y_test = y_test.values
        y_test = np.reshape(y_test,(y_test.shape[0],))
        y_train = np.reshape(y_train,(y_train.shape[0],))
        return X_train.values,X_test.values,y_train,y_test

    def get_columns_name_after_remove(self):
        f = FinalDataSet()
        series = f.series_matrix
        # Removing the highly correlated columns i.e >0.8
        remove_list = list(set(self.load_pickle("final_dataset/to_remove")))
        remove_list = series.columns[remove_list]
        series = series.drop(columns=list(remove_list))
        return series.columns
