import os,sys
sys.path.append(os.path.abspath(""))
sys.path.append(os.path.abspath("../"))
import multiprocessing,time
import numpy as np
from numba import jit
import math,pickle

from preprocessing.Normalize import Normalize

def add_pickle(object,filename):
    with open("feature_selection/pickle/"+filename+'.pickle', 'wb') as f:
        pickle.dump(object, f)

def load_pickle(filename):
#     print(filename)
    with open("feature_selection/pickle/"+filename+'.pickle','rb') as f:
        loaded_obj = pickle.load(f)

@jit
def corref(x,y):
    corr_val = np.corrcoef(x,y)[0,1]
    threshold = 0.8
    if(corr_val>=threshold):
        return (True,corr_val)
    return (False,corr_val)

# @jit
def thread(x,normal_matrix):
    ret = []
    for y in range(x):
        if x!=y:
            val = corref(normal_matrix[:,x],normal_matrix[:,y])
            if val[0]:
                ret.append([x,y,val[1]])
    return ret

def job(arg_list):
    process_no = arg_list[0]
    beg = arg_list[1]
    end = arg_list[2]
    normal_matrix = arg_list[3]
    print("START Process no ::: ",process_no,"\tJob From *** ",beg," -- ",end)
    t=time.time()
    ret = []
    for x in range(beg,end,1):
        val = thread(x,normal_matrix)
        ret+=val
    add_pickle(ret,"process_"+str(beg)+"-"+str(end))
    print("******END Process no ::: ",process_no,"   END*****")
    print("Process no",process_no," \t time ::: ",time.time()-t)
    
if __name__=="__main__":
    t = time.time()
    n = Normalize()
    normal_matrix = n.get_normalized_data()
    matirx_cols = list(normal_matrix.columns)
    matrix_index = list(normal_matrix.index)
    # normal_matrix = normal_matrix.to_numpy()
    normal_matrix = np.array(normal_matrix)
    print("NORMALIZED TIME ::: ",time.time()-t)
    step = 500
    process_no = 1
    p = multiprocessing.Pool(processes=6)
    args = []
    for i in range(0,len(normal_matrix[0]),step):    
        upto = i+step
        if upto> len(normal_matrix[0]):
            upto = len(normal_matrix[0])
        try:
            load_pickle("process_"+str(i)+"-"+str(upto))
        except FileNotFoundError as e:
            args.append(np.array([process_no,i,upto,normal_matrix]))
        process_no+=1
#     for x in args:
#         print(x)
    p.map(job, args)
    p.close()
        # print(data)
    
    