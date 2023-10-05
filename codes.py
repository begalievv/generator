
from templater import TEMPLATE_FUNCS
from templaterPgSQL import TEMPLATE_FUNCS as TEMPLATEPGSQL
from settings import SUBD




def fill_file(text, table_data):
    res = ""
    while(True):
        open_index = text.find('@|')
        if(open_index == -1): break
        before_text = text[:open_index]

        close_index = text.find('|@')
        if(close_index == -1): raise Exception("Нет закрывающей скобки!!!")
        func_name = text[open_index + 2: close_index]

        res += before_text 
        if(SUBD == "MSSQL"):
            template = TEMPLATE_FUNCS[func_name](table_data)
        else:
            template = TEMPLATEPGSQL[func_name](table_data)

        res += template 

        text = text[close_index + 2:]
    res += text
        
    return res


def fill_bfile(text, tables_data):
    res = ""
    while(True):
        open_index = text.find('@|')
        if(open_index == -1): break
        before_text = text[:open_index]

        close_index = text.find('|@')
        if(close_index == -1): raise Exception("Нет закрывающей скобки!!!")
        func_name = text[open_index + 2: close_index]

        res += before_text 
        template = ''
        for table_data in tables_data:
            if(SUBD == "MSSQL"):
                template += TEMPLATE_FUNCS[func_name](table_data)
            else:
                template += TEMPLATEPGSQL[func_name](table_data)
        res += template

        text = text[close_index + 2:]
    res += text
    return res