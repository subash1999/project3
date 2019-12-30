import sqlite3
import pickle
import sys
import traceback
from numba import jit,vectorize


class Corr():    
    def __init__(self):
        self.path = 'storage/'
        self.db = 'storage.db'
        self.table_name = "corr"
        self.conn = sqlite3.connect(self.path+self.db)
        # Testing Below
        # self.db = ":memory:"#for testing purpose
        # self.conn = sqlite3.connect(self.db)
        

        self.c = self.conn.cursor()

        if(self.check_if_table_exists(self.table_name) == False):
            self.create_corr_table()
        self.conn.commit()

    def create_corr_table(self)->bool:
        try:
            query = """CREATE TABLE `{table_name}`(
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `gene_id_1` TEXT,
                `gene_id_2` TEXT,
                `value` REAL,
                `corr_type` TEXT,
                `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
            )""".format(table_name=self.table_name)
            self.c.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            # traceback.print_exc(file=sys.stdout)
            print(e)
            return False

    def drop_corr_table(self)->bool:
        try:
            query = "DROP TABLE IF EXISTS`{table_name}`".format(table_name=self.table_name)
            self.c.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
    # @jit
    def add_corr(self,gene_id_1,gene_id_2,value,corr_type):
        try :
            if(self.check_if_table_exists(self.table_name) == False):
                self.create_objects_table()
            query = '''INSERT INTO `{table_name}` (`gene_id_1`,`gene_id_2`,`value`,`corr_type`)
                VALUES(
                    '{gene_id_1}',
                    '{gene_id_2}',
                    '{value}',
                    '{corr_type}'
                )'''.format(table_name=self.table_name,gene_id_1=gene_id_1,gene_id_2=gene_id_2,
                value=value,corr_type=corr_type)
            self.c.execute(query)
            # self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False 
    
    def delete_row(self,id:int):
        try:
            query = "DELETE FROM `{table_name}` WHERE `id`={id}".format(table_name=self.table_name,id=id)
            self.c.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
    
    def get_corr(self,id : int):
        query = "SELECT * FROM `{table_name}` WHERE `id`={id}".format(table_name=self.table_name,id=id)
        self.c.execute(query)
        rows = self.c.fetchall()
        
        return self.rows_to_correlation(rows)
    
    def get_all(self)->list:
        query = "SELECT * FROM `{table_name}` ".format(table_name=self.table_name)
        self.c.execute(query)
        rows = self.c.fetchall()
        return self.rows_to_correlation(rows)
    
    def rows_to_correlation(self,rows :list)->list:
        corr_object_list = []
        for row in rows:
            corr_object_list.append(self.Correlation(row[0],row[1],row[2],row[3],row[4],row[5]))
        return corr_object_list

    
    def check_if_table_exists(self,table_name : str):
        query = "SELECT count(name) FROM `sqlite_master` WHERE `type`='table' AND name='"+table_name+"'"
        self.c.execute(query)
        if self.c.fetchone()[0]>=1 : 
            return True
        else :
            return False
    
    def search_all(self,keyword :str,print_result=True):
        print("*********"*4,"Searching By Gene_id_1","*********"*4)
        rows = list(self.search_by_gene_id_1(keyword,print_result))
        print("*********"*4,"Searching By Gene_id_2","*********"*4)
        rows.append(list(self.search_by_gene_id_2(keyword,print_result)))
        print("*********"*4,"Searching By Correlation Type","*********"*4)
        rows.append(list(self.search_by_corr_type(keyword,print_result)))
        return rows

    def search_by_gene_id_1(self,keyword : str,print_result = True):
        query = '''SELECT * FROM `{table_name}` WHERE `gene_id_1` LIKE '%{keyword}%'
        '''.format(table_name=self.table_name,keyword=keyword)
        self.c.execute(query)
        rows = self.c.fetchall()
        rows = self.rows_to_correlation(rows)
        if (print_result):
            self.print_result(rows,"gene_id_1",keyword)
        return rows
    
    def search_by_gene_id_2(self,keyword : str,print_result = True):
        query = '''SELECT * FROM `{table_name}` WHERE `gene_id_2` LIKE '%{keyword}%'
        '''.format(table_name=self.table_name,keyword=keyword)
        self.c.execute(query)
        rows = self.c.fetchall()
        rows = self.rows_to_correlation(rows)
        if (print_result):
            self.print_result(rows,"gene_id_2",keyword)
        return rows
    
    def search_by_corr_type(self,keyword : str,print_result = True):
        query = '''SELECT * FROM `{table_name}` WHERE `corr_type` LIKE '%{keyword}%'
        '''.format(table_name=self.table_name,keyword=keyword)
        self.c.execute(query)
        rows = self.c.fetchall()
        rows = self.rows_to_correlation(rows)
        if (print_result):
            self.print_result(rows,"corr_type",keyword)
        return rows
    

    def print_result(self,rows,result_for = "",keyword = ""):
        print("-----"*8)
        print("-----"*8)
        if(result_for != "" or keyword != ""):            
            print("Search Result Found for ",result_for ," = ",keyword)
        print("Results Found : ",len(rows))
        for x in rows:
            if type(x) == type(self.Correlation()):
                print("____ROW___START____")
                print("ID : ",x.id)
                print("Gene ID 1 : ",x.gene_id_1)
                print("Gene ID 2 : ",x.gene_id_2)
                print("Value : ",x.value)
                print("Correlation Type : ",x.corr_type)
                print("Created at : ",x.created_at)
                print("____ROW___END____")
            else : 
                print("____ROW___START____")
                print("ID : ",x[0])
                print("Gene ID 1 : ",x[1])
                print("Gene ID 2 : ",x[2])
                print("Value : ",x[3])
                print("Correlation Type : ",x[4])
                print("Created at : ",x[5])
                print("____ROW___END____")
        print("-----"*8)
        print("-----"*8)
    def check_if_val_pair_exists(self,x,y,corr_type):
        query = '''SELECT * FROM `{table_name}` WHERE ((`gene_id_1` = "{x}" AND `gene_id_2` = "{y}")
        OR (`gene_id_2` = "{x}" AND `gene_id_1` = "{y}")) AND `corr_type` = "{corr_type}"
        '''.format(table_name=self.table_name,x=x,y=y,corr_type=corr_type)
        self.c.execute(query)
        rows = self.c.fetchall()
        if(len(rows)>=1):
            return self.rows_to_correlation(rows)
        return False
    
    def commit(self):
        self.conn.commit()

    # @jitclass()
    class Correlation():
        
        def __init__(self,id=None,gene_id_1 =None,gene_id_2=None,value=None,corr_type=None,created_at=None):
            self._id = id
            self._gene_id_1 = gene_id_1
            self._gene_id_2 = gene_id_2
            self._value = value
            self._corr_type = corr_type
            self._created_at = created_at
        
        @property
        def id(self):
            return self._id
        
        @property
        def gene_id_1(self):
            return self._gene_id_1
        
        @property
        def gene_id_2(self):
            return self._gene_id_2
        
        @property
        def value(self):
            return self._value
        
        @property
        def corr_type(self):
            return self._corr_type
        
        @property
        def created_at(self):
            return self._created_at


        
        



