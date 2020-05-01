# from SmartDjango import Pager
import datetime

from SmartDjango.models import Pager

time_d_pager = Pager(compare_field='time', ascend=False)


def last_timer(last):
    if last == 0:
        return datetime.datetime.now()
    else:
        return datetime.datetime.fromtimestamp(last)
