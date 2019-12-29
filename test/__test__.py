from multiprocessing import Process, Value, Array
import numpy as np
import time
import concurrent.futures

def multithread(i,process_count,thread_count):
    # time.sleep(0.0001)
    print(i*i)
    # print("Process Count :",process_count,"-- Thread Count : ",thread_count,"Result",i**i)

def multiprocess(x,process_count):
    print("Process  : ",process_count)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as execute:
        thread_count = 0
        for i in range(0,10,1):
            execute.submit(multithread,i,process_count,thread_count)
        thread_count+=1

if __name__ == "__main__":
    t = time.time()
    step = 100
    process_count =0
    processes = []
    for i in range(0,100,1):
        x=i
        for x in range(i,(i+step),1):
            p = Process(target=multiprocess,args=([x,process_count]))
            processes.append(p)
            p.start() 
            process_count+=1
    for process in processes:
        process.join()
    print("Total Time required : ",time.time()-t)
