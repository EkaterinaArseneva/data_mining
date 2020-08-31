import datetime
"""
my_date = datetime.datetime.fromisoformat("2020-06-30T13:33:00+03:00")
#my_date = my_date.replace(tzinfo=None)
my_date_2 = datetime.datetime.now(tz=datetime.timezone.utc)
if my_date > datetime.datetime(1, 1, 1):
    print ('wow')
else: print ('fuck')
print(my_date, '\n', my_date_2)
"""

datetime.datetime(1,1,1, tzinfo=datetime.timezone.utc)