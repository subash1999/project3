from scipy import stats
import numpy as np
import pandas as pd
import sys
sys.path.append('../')
import os
sys.path.append(os.path.abspath(""))
from final_dataset.FinalDataSet import FinalDataSet

class Normalize():
    def __init__(self):
        pass
    
    def get_normalized_data(self):
        f = FinalDataSet()
        series = f.series_matrix.copy()
        del f
        return series