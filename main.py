import os, shutil
from funcs import get_tables
from codes import fill_file

def main():

    for folder in os.walk("result"):
        if(folder[0] == "result"): continue
        shutil.rmtree(folder[0])

    tables_data = get_tables()

    for table_data in tables_data[:7]:
        table_name = table_data["table"]

        for folder in os.walk("source"):
            if(folder[0] == "source"): continue
            if not os.path.exists(folder[0].replace('source', 'result')):
                os.makedirs(folder[0].replace('source', 'result'))

            path_dir = folder[0].replace('source', 'result') + '/' + table_name
            if not os.path.exists(path_dir):
                os.makedirs(path_dir)

            for file in folder[2]:
                with open(folder[0] + '/' + file, encoding='utf-8') as f:
                    cont = f.read()
                    
                    text = fill_file(cont, table_data)

                file_name =  file.replace('@table_name@', table_name)
                f = open(path_dir + "/" + file_name, "a", encoding='utf-8')
                
                f.write(text)
                f.close()




main()