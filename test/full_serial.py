import sys,os,time
sys.path.append(os.path.abspath(""))
from multiprocessing import Process, Value, Array
import numpy as np
import time
import concurrent.futures
from preprocessing.Normalize import Normalize
from scipy.stats.stats import pearsonr
from storage.Corr import Corr
import helper.SeriesHelper as series_helper 
import concurrent.futures
import multiprocessing


# /////////////////////////////////////////////////// #
# /////////////////////////////////////////////////// #

def check_repetation(x,y):
    rows = c.check_if_val_pair_exists(x,y,corr_type)
    if rows == False:
        return False
    return True
# /////////////////////////////////////////////////// #
# /////////////////////////////////////////////////// #

def multithread(x_col,y_col,normal_matrix,t_count): 
    t1 = time.time()
    c = Corr()
    pearson_corr,p = pearsonr(normal_matrix[x_col].to_numpy(),normal_matrix[y_col].to_numpy())
    # print(count,"Pearson single : ",time.time()-t1)
    c.add_corr(x_col,y_col,pearson_corr,"pearson")
    # print(count,"add Corr Single : ",time.time()-t1)
    res = x_col+",",y_col," . Done in "+str(time.time()-t1)+"\n"
    # print(res,end=" ")
    print("Thread Finish no :",+t_count," of ",len(list(normal_matrix.columns))**2)
    del res
    del c

def multiprocess(x_col,normal_matrix,p_count):
    t_count = (p_count-1)*len(list(normal_matrix.columns))

    # with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
    #     for y in range(0,len(list(normal_matrix.columns)),1):
    #         t_count+=1
    #         executor.submit(multithread,x_col,normal_matrix.columns[y],normal_matrix,t_count)

    t_count = (p_count-1)*len(list(normal_matrix.columns))
    for y in range(0,len(list(normal_matrix.columns)),1):
        t_count+=1
        multithread(x_col,normal_matrix.columns[y],normal_matrix,t_count)


# if __name__ == '__main__':   
tot = time.time()
t_count = 0
p_count = 0

# ______________________________________________________ #
# ______________________________________________________ #
t0 = time.time()
corr_type = "pearson"
n = Normalize()
normal_matrix = n.get_normalized_data()
matrix_cols = list(normal_matrix.columns)
print("Normalize : ",time.time()-t0)
t0 = time.time()
del n
del Normalize
print("Delete : ",time.time()-t0)
# ______________________________________________________ #
# ______________________________________________________ #   
##########################################################
##########################################################
t0 = time.time()
print("****Emptying the table****")
c = Corr()
c.drop_corr_table()
c.create_corr_table()
del c
print("Corr Table Create and Delete Time : ",time.time()-t0)
#########################################################
########################################################

#*****************************************************#
#-----------------------------------------------------#


beg = 0    
step = 1

end = len(matrix_cols)
end = 1
p_count = 0
for i in range(beg,end,step):
    p_time = time.time()
    processes = []
    # for i2 in range(i,(i+step),1):
    #     p_count +=1
    #     print("Process Init : ",p_count, " of ",end)
    multiprocess(matrix_cols[i],normal_matrix,p_count)
    #     processes.append(p)
    #     p.start()             
    # for process in processes:
    #     process.join()
    print("*PROCESS *",i,"--",i+step," END")
    print("TIME REQ PER PROCESS :::: ",time.time()-p_time)


print("Total : ",time.time()-tot)


