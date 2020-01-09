import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')
pd.options.display.max_columns = None

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_selection import RFECV
from sklearn.model_selection import train_test_split
import multiprocessing
import sys,os
# sys.path.append(os.path.abspath("../"))
# from preprocessing.Normalize import Normalize
# import helper.SeriesHelper as series_helper
import time
import pickle
import dask.dataframe as dd
from dask.distributed import Client
import warnings





def worker(col_beg,col_end,correlation_matrix,return_list,process_count):
    '''worker function'''
    t = time.time()
    print("*****"*5,process_count," Process started","*****"*5,)
    correlated_features = []
    for i in range(col_beg,col_end,1):
        for j in range(i):
            if j!=0:
                try:
                    if abs(correlation_matrix.iloc[i, j]) > 0.8:
                        colname = correlation_matrix.columns[i]
                        correlated_features.append([colname,correlation_matrix.iloc[i, 0],correlation_matrix.iloc[i, j]])
                except Exception as e:
                    print("*****"*10,"EXCEPTION","*****"*10)
                    print("Exception :: ",e)
                    print("i,j :: ",i,j)
                    print(f'Number of rows: {len(correlation_matrix):,}.')
                    print("Number of Columns :: ",str(len(correlation_matrix.columns)))
                    print("*****"*10,"END EXCEPTION","*****"*10)
    return_list += correlated_features
    print("--"*5,"No of features to remove : ",str(len(return_list)),"--"*5)
    print("Time Required  for loop : ",time.time()-t)
    print(process_count," Chunk Process Ended")
    print("*****"*5,"  ",process_count," CHUNK END ","  ","*****"*5)


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    t = time.time()
    # client = Client()
    print("***** CLIENT *****")
    # print(client)
    manager = multiprocessing.Manager()
    return_list = manager.list()
    
    corr_time = time.time()
    print("Start Reading Correlation Matrix")
    correlation_matrix = dd.read_csv("correlation.csv")
    # correlation_matrix = pd.read_csv("correlation.csv")
    a= correlation_matrix.shape
    print("Correlation Matrix Shape ::: ",a[0].compute(),a[1])
    print("Corr Matrix Read Time :: ",time.time()-corr_time)
    del corr_time

    jobs = []
    step = 4000
    process_count = 1

    for i in range(0,len(correlation_matrix.columns),step):
        p = multiprocessing.Process(target=worker, args=(i,i+step,correlation_matrix,return_list,process_count))
        jobs.append(p)
        p.start()
        process_count+=1
    for proc in jobs:
        proc.join()
    
    for x in range(0,len(return_list),1):
        print(x,"\t",x)
    print("RETURN LIST COUNT : ",len(return_list))
    with open('return_list.list', 'wb') as save_file: 
        # Step 3
        pickle.dump(return_list, save_file)
    print("TOTAL TIME REQURIED :: ",time.time()-t)
