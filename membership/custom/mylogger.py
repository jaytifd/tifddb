import datetime
import sys
def p(*item):
    print ("DEBUG: ", str(datetime.datetime.now()), " - ",*item)
    logfile = open('debuglog.txt', 'a', encoding='utf-8')
    print ("DEBUG: ", str(datetime.datetime.now()), " - ",*item, file=logfile)

