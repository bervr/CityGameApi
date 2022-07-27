import datetime
import time


a = datetime.datetime.now()
print(a)

u=a.timestamp()
print(u)

o = datetime.datetime.fromtimestamp(u)
print(o)

s=17677.96704000000

print(s)

print(datetime.timedelta(seconds=s))

