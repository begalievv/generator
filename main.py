import os, shutil
from funcs import get_tables
from codes import fill_file, fill_bfile

def main():

    for folder in os.walk("result"):
        if(folder[0] == "result"): continue
        shutil.rmtree(folder[0])

    tables_data = get_tables()
    tree_folders = []
    for table_data in tables_data:
        table_name = table_data["table"]

        for folder in os.walk("source"):
            if(folder[0] == "source"): continue
            if(folder[0] == "source\\bfiles"): continue
            if(folder[1] != []):
                tree_folders = folder[1]
            
            if(len(folder[0].split('\\')) != 3):
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

            for tree_fold in tree_folders:
                if(tree_fold in folder[0]):
                    folder_name = table_name + '/' + tree_fold.replace('@table_name@', table_name)
                    full_path = folder[0].replace(tree_fold, folder_name)
                    for file in folder[2]:
                        with open(folder[0] + '/' + file, encoding='utf-8') as f:
                            cont = f.read()
                            text = fill_file(cont, table_data)

                        file_name =  file.replace('@table_name@', table_name)
                        if not os.path.exists(full_path.replace('source', 'result')):
                            os.makedirs(full_path.replace('source', 'result'))
                        f = open((full_path + '/' + file).replace('source', 'result'), "a", encoding='utf-8')
                        f.write(text)
                        f.close()

    for folder in os.walk("source/bfiles"):
        if not os.path.exists(folder[0].replace('source', 'result')):
            os.makedirs(folder[0].replace('source', 'result'))
        
        for file in folder[2]:
            with open(folder[0] + '/' + file, encoding='utf-8') as f:
                cont = f.read()
                
                text = fill_bfile(cont, tables_data)

            f = open('result/bfiles/' + file, "a", encoding='utf-8')
            
            f.write(text)
            f.close()


main()