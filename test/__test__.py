import sys,os,time
sys.path.append(os.path.abspath(""))
tot = time.time()
t0 = time.time()
from preprocessing.Normalize import Normalize
from scipy.stats.stats import pearsonr
from storage.Corr import Corr
import helper.SeriesHelper as series_helper
import concurrent.futures
print("import : ",time.time()-t0)

# ______________________________________________________ #
# ______________________________________________________ #
t0 = time.time()
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
print("Corr : ",time.time()-t0)
#########################################################
########################################################

#*****************************************************#
#-----------------------------------------------------#
corr_type = "pearson"
count = 0
def add_corr(x,y,count):    
    t1 = time.time()
    pearson_corr,p = pearsonr(normal_matrix[x],normal_matrix[y])
    # print(count,"Pearson single : ",time.time()-t1)
    t1 = time.time()
    c.add_corr(x,y,pearson_corr,corr_type)
    # print(count,"add Corr Single : ",time.time()-t1)
#-----------------------------------------------------#
#*****************************************************#

# /////////////////////////////////////////////////// #
# /////////////////////////////////////////////////// #

def check_repetation(x,y):
    rows = c.check_if_val_pair_exists(x,y,corr_type)
    if rows == False:
        return False
    for r in rows:
        c.delete_row(r.id)
    return False
# /////////////////////////////////////////////////// #
# /////////////////////////////////////////////////// #

beg = 0

end = int(len(list(normal_matrix.columns)))
# done until now 1*end, do it 88 per times.
step = 100

# end = 10

for i in range(beg,end,step):
    t0 = time.time()
    for x in list(normal_matrix.columns)[i:(i+step)]:
        t1=time.time()
        pearson_corr,p = pearsonr(normal_matrix[x],series_helper.get_relapse_value_from_series_matrix(normal_matrix))
        print("Find corr ",time.time()-t1)
        t1=time.time()
        y="relapse"
        c.add_corr(x,y,pearson_corr,corr_type)
        print("add corr ",time.time()-t1)        
        count+=1
        print("Finished for ",x,"  Count : ",count)
    print("Loop ",i,"--",(i+step-1)," Execute all : ",time.time()-t0)


t0 = time.time()

    
print("Total : ",time.time()-tot)