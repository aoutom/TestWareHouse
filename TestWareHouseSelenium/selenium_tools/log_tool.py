import logging
import datetime
import os
class CreateLog():
    def __init__(self):
        self.logger=logging.getLogger()
        self.logger.setLevel(logging.INFO)
        consle=logging.StreamHandler()
        self.logger.addHandler(consle)
        base_file=os.path.join(os.path.split(os.path.dirname(__file__))[0],'logs')
        #print(base_file)
        time_file=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+".log"
        file_name=os.path.join(base_file,time_file)
        self.file_handle=logging.FileHandler(file_name)

        formatter = logging.Formatter("%(asctime)s %(filename)s --> %(funcName)s %(levelno)s %(levelname)s --> %(message)s")

        self.file_handle.setFormatter(formatter)
        self.logger.addHandler(self.file_handle)

    def get_log(self):
        return self.logger
    def close_log(self):
        self.file_handle.close()
        self.logger.removeHandler(self.file_handle)
if __name__=="__main__":
    user=CreateLog()
    log=user.get_log()
    log.info("TTTTT")
    user.close_log()


