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
    with open("feature_selection/pickle/"+filename+'.pickle') as f:
        loaded_obj = pickle.load(f)

@jit
def corref(x,y):
    corr_val = np.corrcoef(x,y)[0,1]
    threshold = 0.9
    if(corr_val>=threshold):
        return True
    return False

# @jit
def thread(x,normal_matrix):
    ret = []
    for y in range(0,len(normal_matrix[0]),1):
        if x!=y:
            if corref(normal_matrix[:,x],normal_matrix[:,y]):
                ret.append(np.array([x,y]))
    return np.array(ret)

def job(arg_list):
    process_no = arg_list[0]
    beg = arg_list[1]
    end = arg_list[2]
    normal_matrix = arg_list[3]
    print("START Process no ::: ",process_no,"\tJob From *** ",beg," -- ",end)
    t=time.time()
    ret = np.array([])
    for x in range(beg,end,1):
        val = thread(x,normal_matrix)
        ret = np.append(ret,val)
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
    step0 = 100
    process_no = 1
    for i in range(0,len(normal_matrix[0]),step0):    
        beg = i
        end = i+step0
        step = 20
        p = multiprocessing.Pool(processes=math.ceil(end/step))
        args = []
        for x in range(beg,end,step):
            args.append(np.array([process_no,x,(x+step),normal_matrix]))
            process_no+=1
        # print(args[0])
        p.map(job, args)
        p.close()
        # print(data)
    
    