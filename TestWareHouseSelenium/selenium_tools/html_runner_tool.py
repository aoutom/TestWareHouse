import HTMLTestRunner
import datetime
import os
def html_runner(suite,file=None,add_name=None,title="test",description=u"测试",verbosity=2):
    if not file:
        file_path=os.path.join(os.path.split(os.path.dirname(__file__))[0],'html_report')
        if not add_name:
            filename=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+".html"
        else:
            filename=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S_")+add_name+".html"
        file_name=os.path.join(file_path, filename)
    else:
        file_name=file

    f = open(file_name,'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=f,title=title,description=description,verbosity=verbosity)
    runner.run(suite)
    f.close()
    return True

