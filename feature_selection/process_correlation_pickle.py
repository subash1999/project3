import os,sys
sys.path.append(os.path.abspath(""))
sys.path.append(os.path.abspath("../"))
import multiprocessing,pandas.tests.io.msgpack.test_extension

import math,pickle
import numpy as np
import time
from preprocessing.Normalize import Normalize

def add_pickle(object,filename):
    with open("feature_selection/pickle/"+filename+'.pickle', 'wb') as f:
        pickle.dump(object, f)

def load_pickle(filename):
    with open("feature_selection/pickle/"+filename+'.pickle','rb') as f:
        loaded_obj = pickle.load(f)
    return loaded_obj

    
def job(args):
    t = time.time()
    pickle = args[0]
    to_keep = args[1]
    to_remove = args[2]
    process_no = args[3]
    start = args[4]
    end = args[5]
    print("START Process NO : ",process_no,"\t START : ",start,"    END : ",end,"\nPickle no :: ",len(pickle))

    c = 1
    for x in pickle:
        print("Process no ",process_no," \t Pickle ",c,"Length of x ",len(x))
        c+=1
        

        for y in x:
            # print("Process ",process_no,"\t Length of x ",len(x))
            if (y[0] not in to_remove):
                to_keep.append(y[0])
                
            if (y[1] not in to_keep):
                to_remove.append(y[1])
        print("Time for Process ",process_no," Count ::",c)
    print(process_no,"*******END Process NO : ",process_no,"\t START : ",start,"    END : ",end,"*******",process_no)
    print("Process no :: ",process_no,"\t Time Required :: ",time.time()-t)
if __name__=="__main__":
    print("Start")
    # n = Normalize()
    # normal_matrix = n.get_normalized_data()
    # normal_matrix = np.array(normal_matrix)
    # print("Normal Matrix")

    step = 500
    pickles=[]
    print("Getting Pickles")
    for i in range(0,22215,step):  
        upto = i+step
        if upto > 22215:
            upto = 22215
        pickles.append(load_pickle("process_"+str(i)+"-"+str(upto)))
    print("Finished getting Pickles, Length of Pickle = ",len(pickles))

    step = 5
    process_no = 1
    p = multiprocessing.Pool()
    manager = multiprocessing.Manager()
    to_keep = manager.list()
    to_remove = manager.list()
    args = []
    c = 1
    tot = 0
    for pickle in pickles:
        # print(p)
        print("Count :: ",c," Length :: ",len(pickle))
        tot += len(pickle)
        c+=1
    print("Total Count :: ",tot)
    print("For Loop Starts")
    for i in range(0,len(pickles),step):    
        print("For Loop : ",i)
        upto = i+step
        if upto> len(pickles):
            upto = len(pickles)
        args.append([pickles[i:upto],to_keep,to_remove,process_no,i,upto])
        process_no+=1
#     for x in args:
#         print(x)
    p.map(job, args)
    add_pickle(to_keep,"to_keep")
    add_pickle(to_remove,"to_remove")
    p.close()
