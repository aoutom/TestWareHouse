from django.forms import model_to_dict
def choice_method(test):
    result=[]
    #result.append(test.subject)
    #result.append(test.point)
    result.append(test[3])#style
    result.append(test[4])#desc
    result.append(test[5])#answer
    result.append(test[6])#explain
    select=[]
    l=11#select_a
    label=["A","B","C","D","E","F","G","H"]
    for i in range(test[10]):
        select.append([label[i],test[l+i]])
    result.append(select)
    result.append(test[0])
    return result

def check_method(test):
    result=[]
    #result.append(test.subject)
    #result.append(test.point)
    result.append(test[3])
    result.append(test[4])
    result.append(test[5].split(";;;"))
    result.append(test[6])
    select=[]
    l=11#select_a
    label=["A","B","C","D","E","F","G","H"]
    for i in range(test[10]):
        select.append([label[i],test[l+i]])
    result.append(select)
    result.append(test[0])
    return result

def text_method(test):
    result=[]
    #result.append(test.subject)
    #result.append(test.point)
    result.append(test[3])#style
    result.append(test[4])#desc
    result.append(test[5])#answer
    result.append(test[6])#explain
    select=[]
    l=11
    label=["A","B","C","D","E","F","G","H"]
    for i in range(test[10]):
        select.append([label[i],test[l+i].split(";;;")])
    result.append(select)
    result.append(test[0])
    return result




