import datetime
import sys
import inspect

def p(*item):
    curframe = inspect.currentframe()
    frame=sys._getframe(1).f_code.co_filename+":"+str(sys._getframe(1).f_lineno)+" "+sys._getframe(1).f_code.co_name
    try:
        print ("DEBUG: ", str(datetime.datetime.now()), " - ", frame,*item)
    except:
        print ("ERROR PRINTING")
    logfile = open('debuglog.txt', 'a')
    print ("DEBUG: ", str(datetime.datetime.now()), " - ", frame, *item, file=logfile)
    logfile.close()

