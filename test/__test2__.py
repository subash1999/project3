
import sys,os
sys.path.append(os.path.abspath(""))

from storage.Corr import Corr
c = Corr()
print(len(c.get_all()))
# from preprocessing.Normalize import Normalize
# n = Normalize()
# print(len(n.get_normalized_data().columns))
