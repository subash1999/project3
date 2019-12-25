from storage.Storage import Storage
s = Storage()
rows = s.get_table()
s.print_search_result(rows,"Table","No keyword")
