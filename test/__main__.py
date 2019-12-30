import sys,os,time
sys.path.append(os.path.abspath(""))
from preprocessing.Normalize import Normalize
from scipy.stats.stats import pearsonr
from storage.Corr import Corr
import helper.SeriesHelper as series_helper 
import concurrent.futures
import multiprocessing

def add_corr(x,y,count):    
    t1 = time.time()
    c = Corr()
    pearson_corr,p = pearsonr(normal_matrix[x],normal_matrix[y])
    # print(count,"Pearson single : ",time.time()-t1)
    c.add_corr(x,y,pearson_corr,corr_type)
    # print(count,"add Corr Single : ",time.time()-t1)
    res = str(count)+". Done in "+str(time.time()-t1)+"\n"
    print(res,end="")
    del res
    del c
    
#-----------------------------------------------------#
#*****************************************************#

# /////////////////////////////////////////////////// #
# /////////////////////////////////////////////////// #

def check_repetation(x,y):
    rows = c.check_if_val_pair_exists(x,y,corr_type)
    if rows == False:
        return False
    return True
# /////////////////////////////////////////////////// #
# /////////////////////////////////////////////////// #



if __name__ == '__main__':   
    tot = time.time()

    # ______________________________________________________ #
    # ______________________________________________________ #
    t0 = time.time()
    corr_type = "pearson"
    n = Normalize()
    normal_matrix = n.get_normalized_data()
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
    print("Corr Time : ",time.time()-t0)
    #########################################################
    ########################################################

    #*****************************************************#
    #-----------------------------------------------------#
    

    beg = 0
    end = int(len(list(normal_matrix.columns)))
    # done until now 1*end, do it 88 per times.
    step = 2
    count = 0
    # end = 10
    
    matrix_cols = list(normal_matrix.columns)
    
    for i in range(beg,end,step):
    # multiprocessing_process(0,2,count,matrix_cols)
        processes = []
        for i2 in range(i,(i+step),(i+step)/2):
            p = multiprocessing.Process(target=multiprocessing_process,args=([i2,]))
            processes.append(p)
            p.start() 

        for process in processes:
            process.join()

    print("Total : ",time.time()-tot)


