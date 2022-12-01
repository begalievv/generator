
from templater import TEMPLATE_FUNCS




def fill_file(text, table_data):
    res = ""
    while(True):
        open_index = text.find('@|')
        if(open_index == -1): break
        before_text = text[:open_index]

        close_index = text.find('|@')
        if(close_index == -1): raise Exception("Не закрывающей скобки!!!")
        func_name = text[open_index + 2: close_index]

        res += before_text 
        template = TEMPLATE_FUNCS[func_name](table_data)
        res += template 

        text = text[close_index + 2:]
    res += text
        
    return res