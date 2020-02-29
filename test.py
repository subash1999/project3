from preprocessing.Normalize import Normalize
import helper.SeriesHelper as series_helper
from multiprocessing import Pool,Manager
import numpy as np
import pandas as pd
def job(args):
    X = args[0]
    remove_list = args[1]
    val_list = args[2]
    process_no = args[3]
    for i in range(len(X[0])) : 
        for j in range(0,i):
            val = abs(np.corrcoef(X[:,i],X[:,j])[1][0])
            if val>0.8:
                remove_list.append(j)
                val_list.append([i,j,val])
#         print("For ",i)
    print("Finished Process no , ",process_no)

if __name__=="__main__":
    normal_matrix = Normalize().get_normalized_data()
    cols = normal_matrix.columns
    index = normal_matrix.index
    X = normal_matrix.to_numpy()
    y = series_helper.get_relapse_value_from_series_matrix(normal_matrix)
    manager = Manager()
    remove_list = Manager().list()
    val_list = Manager().list()
    args = []
    process_no = 1
    for i in range(0,X.shape[1],500):
        args.append([X[:,i:i+500],remove_list,val_list,process_no])
        process_no+=1
    print("args finished")
    p = Pool()
    p.map(job,args)