import sqlite3
import pickle
import sys
desc_default = ""
type_default = ".pkl"
class Storage():    
    def __init__(self):
        self.path = 'storage/'
        self.objects_path = 'stroage/objects/'
        # self.db = ":memory:"#for testing purpose
        self.db = 'storage.db'
        self.table_name = "objects"
        self.conn = sqlite3.connect(self.path+self.db)
        

        self.c = self.conn.cursor()

        if(self.check_if_table_exists(self.table_name) == False):
            self.create_objects_table()
        self.conn.commit()

    def create_objects_table(self)->bool:
        try:
            query = """CREATE TABLE {table_name}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT UNIQUE,
                desc TEXT,
                type TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )""".format(table_name=self.table_name)
            self.c.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def add_object(self,object,file_name : str,desc: str = desc_default,type_:str = type_default)->bool:
        try:
            add_object = False
            if(self.check_if_file_name_exists(file_name)):
                print("***WARNING***\n File Name already exists")
                print("Note :: Y or y for 'Yes' and any other key for 'No'")
                val = input("Do you want to override it? If 'No' then system will exit :")
                if(val == 'Y' or val == 'y'):
                    add_object = True
                else:
                    add_object = False
            else : 
                add_object = True

            if(add_object == True):        
                pickle.dump( object, open( self.objects_path+file_name+"."+type_, "wb" ) )
                add_object_in_table(file_name,desc,type_)
            else : 
                sys.exit(0)
            return True
        except Exception as e:
            print(e)
            return False

    def get_object(self,id : int):
        query = "SELECT file_name FROM {table_name} WHERE id={id}".format(table_name=self.table_name,id=id)
        self.c.execute(query)
        rows = self.c.fetchall()
        file_name = rows[0][1]
        return get_object_form_file_name(file_name)

    def get_object_form_file_name(self,file_name : str):
        return pickle.load(open(file_name, 'rb'))

    def search_all(self,keyword :str,print_result=True):
        rows = list(self.search_by_file_name(keyword,False))
        rows.append(list(self.search_by_desc(keyword,False)))
        rows.append(self.search_by_type(keyword,False))
        if (print_result):
            self.print_search_result(rows,"Keyword",keyword)
        return rows
    def search_by_file_name(self,keyword : str,print_result = True):
        query = '''SELECT * FROM {table_name} WHERE file_name LIKE %{keyword}%
        '''.format(table_name=self.table_name,keyword=keyword)
        self.c.execute(query)
        rows = self.c.fetchall()
        if (print_result):
            self.print_search_result(rows,"file_name",keyword)
        return rows

    def search_by_desc(self,keyword : str,print_result=True):
        query = '''SELECT * FROM {table_name} WHERE desc LIKE %{keyword}%
        '''.format(table_name=self.table_name,keyword=keyword)
        self.c.execute(query)
        rows = self.c.fetchall()
        if (print_result):
            self.print_search_result(rows,"desc",keyword)
        return rows

    def search_by_type(self,keyword : str,print_result=True):
        query = '''SELECT * FROM {table_name} WHERE type LIKE %{keyword}%
        '''.format(table_name=self.table_name,keyword=keyword)
        self.c.execute(query)
        rows = self.c.fetchall()
        if (print_result):
            self.print_search_result(rows,"desc",keyword)
        return rows
            
    def add_object_in_table(self,file_name:str,desc:str = desc_default,type_:str = type_default):
        try :
            if(self.check_if_table_exists(self.table_name) == False):
                self.create_objects_table()
            query = '''INSERT INTO {table_name} (file_name,des,type)
            VALUES(
                {file_name},
                {desc},
                {type_}
            )'''.format(table_name=self.table_name,file_name=file_name,desc=desc,type_=type_)
            self.c.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False 
            
    def check_if_table_exists(self,table_name : str):
        query = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='"+table_name+"'"
        self.c.execute(query)
        if self.c.fetchone()[0]>=1 : 
            return True
        else :
            return False

    def check_if_file_name_exists(self,file_name : str):
        query = ''' SELECT count(file_name) FROM {table_name} WHERE 
            file_name='{file_name}' '''.format(table_name=self.table_name,file_name=file_name)
        self.c.execute(query)
        if self.c.fetchone()[0]>=1 : 
            return True
        else :
            return False


    def print_search_result(self,rows,result_for,keyword):
        print("-----"*8)
        print("-----"*8)
        print("Search Result Found for ",result_for ," = ",keyword)
        print("Results Found : ",len(rows))
        for x in rows:
            print("ID : ",x[0])
            print("File Name : ",x[1])
            print("Desc : ",x[2])
            print("Type : ",x[3])
            print("Created at : ",x[4])
        print("-----"*8)
        print("-----"*8)

    def get_table(self,no_of_rows:int = -1):
        query = "SELECT * FROM {table_name}".format(table_name = self.table_name)
        self.c.execute(query)
        if no_of_rows == -1:
            rows = self.c.fetchall()
        else:
            rows = self.c.fetchmany(no_of_rows)
        return rows


        