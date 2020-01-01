
import sys,os
sys.path.append(os.path.abspath(""))

# from storage.Corr import Corr
# c = Corr()
# print(len(c.get_all()))
# c.print_result(c.get_corr(2))
from preprocessing.Normalize import Normalize
n = Normalize()
# print(len(n.get_normalized_data().columns))
print(n.get_normalized_data().isnull().sum().values.sum())