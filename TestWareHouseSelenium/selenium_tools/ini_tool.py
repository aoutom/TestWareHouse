import configparser
import os
class SectionObject():
    def __init__(self, name, content):
        self.name=name
        self.content=content
    def get_option_data(self,  option):
        return self.content.get(self.name, option)

    def get_options(self):
        return self.content.items(self.name)

    def get_options_data(self):
        return [x[1] for x in self.content.items(self.name) ]

    def get_options_name(self):
        return self.content.options(self.name)

    
    def split_data(self, data, label=">"):
        if type(data)==str:
            return data.split(label)
        elif type(data)==list:
            if type(data[0])==str:
                return [x.split(label) for x in data]
            elif type(data)==tuple:
                data_tuple=tuple([])
                for i in data:
                    data_tuple.add((i[0],tuple([i[1].split(label)])))
                return data_tuple


class IniObject():
    def __init__(self, path=None, file="ini_data.ini"):
        if not path:
            path=os.path.join(os.path.split(os.path.dirname(__file__))[0],'ini_data')
        self.content= configparser.ConfigParser()
        self.content.read(os.path.join(path, file), encoding="utf-8")

    def get_option_data(self, section, option):
        return self.content.get(section, option)

    def get_options(self, section):
        return self.content.items(section)

    def get_options_data(self, section):
        return [x[1] for x in self.content.items(section) ]

    def get_options_name(self, section):
        return self.content.options(section)

    def get_sections_name(self):
        return self.content.sections()

    def get_section(self, section):
        return SectionObject(section, self.content)

    def split_data(self, data, label=">"):
        if type(data)==str:
            return data.split(label)
        elif type(data)==list:
            if type(data[0])==str:
                return [x.split(label) for x in data]
            elif type(data)==tuple:
                data_tuple=tuple([])
                for i in data:
                    data_tuple.add((i[0],tuple([i[1].split(label)])))
                return data_tuple



#c=IniObject(file="baidu.ini")
#m=c.get_section("Loginpage")
#print(m.get_option_data('user_name'))
#print(m.split_data(m.get_option_data('user_name')))
#print(m.get_options_data())
#print(m.split_data(m.get_options_data()))

