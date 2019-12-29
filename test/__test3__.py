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
    thread_count = 0
    for i in range(0,10,1):
        multithread(i,process_count,thread_count)
        thread_count+=1


t = time.time()
step = 100
process_count =0
for i in range(0,100,10):
    processes = []
    for x in range(i,(i+step),1):
        multiprocess(x,process_count)
        process_count+=1
print("Total Time required : ",time.time()-t)
