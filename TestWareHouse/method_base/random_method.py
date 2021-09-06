import random

def random_str_code(nums=12):
    base_list="AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
    str_list=""
    for i in range(nums):
        dt=random.randint(0,len(base_list)-1)
        str_list+=base_list[dt]
    return str_list


