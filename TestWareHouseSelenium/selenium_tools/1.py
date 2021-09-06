import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import re
import base64
server = poplib.POP3("pop.qq.com")
server.user("1171596538@qq.com")
server.pass_("xdtemitcfatzjggi")
resp, mails, octets = server.list()
index = len(mails)
resp, lines, octets = server.retr(index)

msg_content = b'\r\n'.join(lines).decode('utf-8')
msg = Parser().parsestr(msg_content)# 解析出邮件:
for i in msg._headers:
    if i[0]=="Subject":
        subject=str(base64.b64decode(re.search("(?<=b\?).+(?=\?)",i[1]).group()),encoding="utf-8")
print(subject)
#print(str(base64.b64decode(msg._payload[0]._payload),encoding="utf-8"))#获得输入的文本
print(msg._payload)#获得输入的文本
print(re.search("(?<=href=').+(?='>)",msg._payload).group())
# 可以根据邮件索引号直接从服务器删除邮件:
# server.dele(index)
server.quit()

