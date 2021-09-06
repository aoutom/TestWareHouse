import os
import ast
def cookie_save( name,dict,path=None):
    if not path:
        path=os.path.join(os.path.split(os.path.dirname(__file__))[0],'cookie')
        path=os.path.join(path,'cookie.txt')
    lines=[]
    with open(path,"r",encoding="utf-8") as f:
        lines=f.readlines()
    find=False
    for i in range(len(lines)):
        line=lines[i].split(":")
        if line[0]==name:
            lines[i]=":".join([name,str(dict)])
            find=True
            break
    if not find:
        lines.append(":".join([name,str(dict)]))
    for i in range(len(lines)):
        lines[i]+="\n"
    with open(path,'w',encoding="utf-8") as f:
        f.writelines(lines)

def cookie_get( name,path=None):
    if not path:
        path=os.path.join(os.path.split(os.path.dirname(__file__))[0],'cookie')
        path=os.path.join(path,'cookie.txt')
    lines=[]
    with open(path,"r",encoding="utf-8") as f:
        lines=f.readlines()
    for i in range(len(lines)):
        line=lines[i].split(":")
        if line[0]==name:
            lt=lines[i]
            print(lt)
            idt=len(name)
            return ast.literal_eval(lt[idt+1:])
    return False

print(cookie_get("A"))
print(type(cookie_get("A")))

a=[1,2,3]

cookie_save("B",a)
print(cookie_get("B"))