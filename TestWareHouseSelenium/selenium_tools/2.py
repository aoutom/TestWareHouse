a=[{'domain': '.baidu.com', 'expiry': 1626963733, 'httpOnly': False, 'name': 'BA_HECTOR', 'path': '/', 'secure': False, 'value': '2sal21aka42ka5c55h1gfis850q'}, {'domain': '.baidu.com', 'httpOnly': False, 'name': 'H_PS_PSSID', 'path': '/', 'secure': False, 'value': '31660_26350'}, {'domain': '.baidu.com', 'expiry': 1658496132, 'httpOnly': False, 'name': 'BAIDUID', 'path': '/', 'secure': False, 'value': '4007B96FBC2DF1ABDA3FEF0DE287D4CC:FG=1'}, {'domain': 'www.baidu.com', 'expiry': 1627824133, 'httpOnly': False, 'name': 'BD_UPN', 'path': '/', 'secure': False, 'value': '12314753'}, {'domain': 'www.baidu.com', 'httpOnly': False, 'name': 'BD_HOME', 'path': '/', 'secure': False, 'value': '1'}, {'domain': '.baidu.com', 'httpOnly': False, 'name': 'BDRCVFR[a_B-xhgHR5m]', 'path': '/', 'secure': False, 'value': 'mk3SLVN4HKm'}, {'domain': '.baidu.com', 'expiry': 3774443779, 'httpOnly': False, 'name': 'PSTM', 'path': '/', 'secure': False, 'value': '1626960132'}, {'domain': '.baidu.com', 'expiry': 3774443779, 'httpOnly': False, 'name': 'BIDUPSID', 'path': '/', 'secure': False, 'value': '4007B96FBC2DF1ABDCF0E9E1E9E25A20'}]
import json 

import fileinput
for i in fileinput.input('1.txt',backup='.bak',inplace=1):
    line=i.split(":=:")
    if line[0]=="A":
        line="OK"

#c=json.dumps(a)
#print(c)

