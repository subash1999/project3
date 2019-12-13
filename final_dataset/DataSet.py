import pandas as pd
import numpy as np

class DataSet():
    def __init__(self):
        self.series_files = [
            "combined_matrix_final_1.csv",
            "combined_matrix_final_2.csv",
            "combined_matrix_final_3.csv",
        ]
        self.clinical_file = "combined_clinical_final.csv"
        self.makeSeriesMatrix()
        self.makeClinical()

    def makeSeriesMatrix(self):
        df_list = []
        for file_name in self.series_files:
            df_list.append(pd.read_csv(file_name))
        self.series_matrix = pd.concat(df_list)
        return self.series_matrix
    
    def makeClinical(self):
        self.clinical  = pd.read_csv(self.clinical_file)
        return self.clinical
    
    def getRelapse(self,str: id):
        pass
    def getSeriesMatrix(self):
        return self.series_matrix
    
    def getClinical(self):
        return self.clinical

        

    