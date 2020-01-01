import os,sys
sys.path.append(os.path.abspath(""))
from preprocessing.Normalize import Normalize
from feature_selection.ChiSquareCustom import ChiSquare
import multiprocessing,time
def test_cols(testColumns,cT,beg,end):
    t = time.time()
    print("Process \t Start ::",beg," \t End ::",end)
    for var in testColumns[beg:end]:
        if(cT.TestIndependence(colX=var)):
            print(var)    
    print("Öne of the process time : ",time.time()-t)
if __name__=="__main__":
    n = Normalize()
    normal_matrix  = n.get_normalized_data()    
    #Initialize ChiSquare Class
    cT = ChiSquare(normal_matrix)
    #Feature Selection
    testColumns = normal_matrix.columns
    processes = []
    p_count = 0
    # multiprocess(i,normal_matrix.to_numpy(),p_count)    
    step=2000    
    for i in range(0,len(testColumns),2000):
        p_count +=1
        print("Process Init : ",p_count, " of ",12)
        p = multiprocessing.Process(target=test_cols,args=([testColumns,cT,i,i+step]))  
        p.start() 
        processes.append(p)                        
    for process in processes:
        process.join()