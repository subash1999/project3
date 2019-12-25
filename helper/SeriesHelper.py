import pandas as pd
import numpy as np
import time
import sys
import os
sys.path.append(os.path.abspath(""))

def get_relapse_value_from_series_matrix(series_matrix : pd.DataFrame):
    relapse_array = []
    for geo_acc in list(series_matrix.index):
        relapse_array.append(get_relapse_value(geo_acc))
    relapse_array  = np.array(relapse_array)
    return relapse_array
        
def get_relapse_value(id_ref : str):
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

    

