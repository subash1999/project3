import pandas as pd
import numpy as np
import time
import sys
import os
sys.path.append(os.path.abspath(""))
print(sys.path)
from preprocessing.Normalize import Normalize

def get_id_ref_by_index(self):
    pass
def get_relapse_value(self,id_ref : str):
        clinical_file = "final_dataset/combined_clinical_final.csv"
        clinical = pd.read_csv(clinical_file)
        df = clinical[clinical.ID == id_ref]
        if df.shape[0] >1 :
            print("There are %d relapse value for same ID in clinical data,Please Check",
            df.shape[0])
            sys.exit(0)
        elif df.shape[0] < 1:
            print("No values present for relapse in the given clinical data")
            # sys.exit(0)
        else : 
            return int(df.iloc[0]["relapse"])

    

