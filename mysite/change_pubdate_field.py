#in django shell (manage.py shell):

from datetime import datetime
from arkadiy39.models import Books

def convert_date(s):
    right_datetime_string=datetime.strptime(s.split(',')[1].strip(),"%d %b %Y %H:%M:%S %z")
    s1=right_datetime_string.strftime('%Y-%m-%d %H:%M:%S%z')
    return s1

    
bb=Books.objects.all()
for b in bb:
    b.pubdate=convert_date(b.pubdate)
    b.save()
    



