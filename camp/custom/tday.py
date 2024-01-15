import datetime
def tday(year):
    if year:
        time=12
        first_day=datetime.datetime(year,11,1).weekday()

        #print("first day:",first_day)
        if first_day==3:
            day=22

        if first_day < 3:
            day=22+(3-first_day)

        if first_day > 3:
            day=22+(6-first_day+4)

        return datetime.datetime(year,11,day,time)
    else: return None

#weekday() = Return the day of the week as an integer, where Monday is 0 and Sunday is 6. For example, date(2002, 12, 4).weekday() == 2, a Wednesday. See also isoweekday().
#Monday     0
#Tuesday    1
#Wednesday  2
#Thursday   3
#Friday     4
#Saturday   5
#Sunday     6

