import sys,os,time
sys.path.append(os.path.abspath(""))
# from multiprocessing import Process, Value, Array
import numpy as np
import time
import concurrent.futures
from preprocessing.Normalize import Normalize
from scipy.stats.stats import pearsonr
from storage.Corr import Corr
# import helper.SeriesHelper as series_helper 
import concurrent.futures
import multiprocessing
from numba import vectorize,jit,njit

# /////////////////////////////////////////////////// #
# /////////////////////////////////////////////////// #

# @njit      # or @jit(nopython=True)
def check_repetation(x,y):
    rows = c.check_if_val_pair_exists(x,y,"pearson")
    if rows == False:
        return False
    return True
# /////////////////////////////////////////////////// #
# /////////////////////////////////////////////////// #

# @njit      # or @jit(nopython=True)
# @jit(parallel=True,fastmath=True)
# @jit
# @jit(parallel=True,fastmath=True)
@njit(fastmath=True)
def multithread(x_col,y_col,normal_matrix,t_count): 
    # t1 = time.time()
    # c = Corr()
    p = np.corrcoef(normal_matrix[:,x_col],normal_matrix[:,y_col])
    # print(count,"Pearson single : ",time.time()-t1)
    # c.add_corr(x_col,y_col,pearson_corr,"pearson")
    # print(count,"add Corr Single : ",time.time()-t1)
    # res = x_col,",",y_col," . Done in "+str(time.time()-t1)+"\n"
    # print(res,end=" ")
    # print("Thread Finish no :",+t_count," of ",len(normal_matrix[0])**2)
    # del res
    # del c
    x_col = int(x_col)
    y_col = int(y_col)
    return np.array([int(x_col),int(y_col),p[0,1]])


def multiprocess_serial(x_col,normal_matrix,p_count):
    t_count = (p_count-1)*len(normal_matrix[0])
    val_array = []

    # with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
    #     for y in range(0,len(list(normal_matrix.columns)),1):
    #         t_count+=1
    #         executor.submit(multithread,x_col,normal_matrix.columns[y],normal_matrix,t_count)

    t_count = (p_count-1)*len(normal_matrix[0])    
    for y in range(0,len(normal_matrix[0]),1):
        t_count+=1
        val_array.append(multithread(x_col,y,normal_matrix,t_count))
    c = Corr()
    for x in val_array:
        x = list(x)
        c.add_corr(str(int(x[0])),str(int(x[1])),x[2],"pearson")
    c.commit()
    del c
        

def multiprocess_thread(x_col,normal_matrix,p_count):
    t_count = (p_count-1)*len(normal_matrix[0])
    futures = []
    val_array = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for y in range(0,len(normal_matrix[0]),1):
            t_count+=1
            futures.append(executor.submit(multithread,x_col,y,normal_matrix,t_count))
        for future in concurrent.futures.as_completed(futures):
            val_array.append(future.result())

    c = Corr()
    for x in val_array:
        x = list(x)
        c.add_corr(str(int(x[0])),str(int(x[1])),x[2],"pearson")
    del c

    # t_count = (p_count-1)*len(normal_matrix[0])
    # for y in range(0,len(normal_matrix[0]),1):
    #     t_count+=1
    #     multithread(x_col,y,normal_matrix,t_count)


def gpu_full_serial(normal_matrix,beg,end,step):
    p_count = 0
    for i in range(beg,end,step):
        p_time = time.time()
        processes = []
        multiprocess_serial(i,normal_matrix,p_count)        
        # for i2 in range(i,(i+step),1):
        #     p_count +=1
        #     print("Process Init : ",p_count, " of ",end)
        #     p = multiprocessing.Process(target=multiprocess,args=([i,normal_matrix.to_numpy(),p_count]))            
        #     processes.append(p)
        #     p.start()             
        # for process in processes:
        #     process.join()
        print("*********GPU FULL SERIAL***********")
        print("*PROCESS *",i,"--",i+step," END")
        print("TIME REQ PER PROCESS :::: ",time.time()-p_time)


def gpu_thread(normal_matrix,beg,end,step):
    p_count = 0
    for i in range(beg,end,step):
        p_time = time.time()
        processes = []
        multiprocess_thread(i,normal_matrix,p_count)        
        # for i2 in range(i,(i+step),1):
        #     p_count +=1
        #     print("Process Init : ",p_count, " of ",end)
        #     p = multiprocessing.Process(target=multiprocess,args=([i,normal_matrix.to_numpy(),p_count]))            
        #     processes.append(p)
        #     p.start()             
        # for process in processes:
        #     process.join()
        print("*********GPU THREAD***********")
        print("*PROCESS *",i,"--",i+step," END")
        print("TIME REQ PER PROCESS :::: ",time.time()-p_time)


def gpu_process(normal_matrix,beg,end,step):
    p_count = 0
    for i in range(beg,end,step):
        p_time = time.time()
        processes = []
        # multiprocess(i,normal_matrix.to_numpy(),p_count)        
        for i2 in range(i,(i+step),1):
            p_count +=1
            print("Process Init : ",p_count, " of ",end)
            p = multiprocessing.Process(target=multiprocess_serial,args=([i,normal_matrix,p_count]))  
            p.start() 
            processes.append(p)                        
        for process in processes:
            process.join()
        print("*********GPU PROCESS***********")
        print("*PROCESS *",i,"--",i+step," END")
        print("TIME REQ PER PROCESS :::: ",(time.time()-p_time)/step)


def gpu_process_thread(normal_matrix,beg,end,step):
    p_count = 0
    for i in range(beg,end,step):
        p_time = time.time()
        processes = []
        # multiprocess(i,normal_matrix.to_numpy(),p_count)        
        for i2 in range(i,(i+step),1):
            p_count +=1
            print("Process Init : ",p_count, " of ",end)
            p = multiprocessing.Process(target=multiprocess_thread,args=([i,normal_matrix,p_count]))            
            processes.append(p)
            p.start()             
        for process in processes:
            process.join()
        print("*********GPU PROCESS THREAD***********")
        print("*PROCESS *",i,"--",i+step," END")
        print("TIME REQ PER PROCESS :::: ",(time.time()-p_time)/step)

def manage_corr_table():
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
    #########################################################

if __name__ == '__main__':   
    # TIMER STARTED
    tot = time.time()

    # MANGE CORRELATION TABLE
    
    
    # NORMAL MATRIX
    normal_time = time.time()
    n = Normalize()
    normal_matrix =  n.get_normalized_data()
    del n
    print("NORMALIZED TIME : ",time.time()-normal_time)
    del normal_time

    # MATRIX COLUMNS
    matirx_cols = normal_matrix.columns
    index = normal_matrix.index
    normal_matrix = normal_matrix.to_numpy()
    print(len(normal_matrix[0]))
    # EXECUTION STARTS HERE
    gpu_full_serial(normal_matrix,0,1,1)
    manage_corr_table()
#     gpu_thread(normal_matrix,0,1,1)
#     st_mul from 0 to 5 
    st_mul = 0
    gpu_process(normal_matrix,0,len(normal_matrix[0]),5)

#     gpu_process_thread(normal_matrix,0,4,4)



    