import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import re
import base64

class EmailObject():
    def __init__(self, msg, ty):
        self.ty=ty
        self.msg=msg

    @property
    def subject(self):
        for i in self.msg._headers:
            if i[0]=="Subject":
                subject=str(base64.b64decode(re.search("(?<=b\?).+(?=\?)",i[1]).group()),encoding="utf-8")
                break
        return subject


    def content(self, pattern=None):
        if sel.ty=="pop.qq.com":
            content=self.msg._payload
        elif sel.ty=="pop.163.com":
            content=self.msg._payload[0]._payload

        if not pattern:
            return content
        else:
            pat = re.compile(pattern)  
            return pat.findall(content)






class Pop3Object():
    def __init__(self, pop_sever, user, password):
        self.server = poplib.POP3(pop_sever)
        self.server.user(user)
        self.server.pass_(password)
class QQ_Email(Pop3Object):

    def get_email(self, index=None, max_length=25):
        resp, mails, octets = self.server.list()
        if not index:
            idt = len(mails)
            resp, lines, octets = self.server.retr(idt)
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            return EmailObject(Parser().parsestr(msg_content),"pop.qq.com")
        elif isinstance(index,int):
            resp, lines, octets = self.server.retr(index)
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            return EmailObject(Parser().parsestr(msg_content),"pop.qq.com")
        elif isinstance(index, str):
            email_list=[]
            idt=len(mails)
            num=max_length
            while num!=0 and idt>=0:
                resp, lines, octets = self.server.retr(idt)
                msg_content = b'\r\n'.join(lines).decode('utf-8')
                msg=Parser().parsestr(msg_content)
                for i in msg._headers:
                    if i[0]=="Subject":
                        subject=str(base64.b64decode(re.search("(?<=b\?).+(?=\?)",i[1]).group()),encoding="utf-8")
                        if subject==str:
                            email_list.append(EmailObject(msg),"pop.qq.com")
                        break
                num-=1
                idt-=1
            return email_list

        else:
            raise ValueError("index must be 'int' or 'str' or None")







