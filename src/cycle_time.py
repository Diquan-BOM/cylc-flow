#!/usr/bin/env python


""" 
CYCLE TIME (YYYYMMDDHH)
"""

# do logical comparisons of cycle times in integer form: int( rt )

# (note "rt" == "reference time" = old cylc name for "cycle time")

import datetime
import re

def _rt_to_dt( rt ):
    return datetime.datetime( 
            int(rt[0:4]), int(rt[4:6]), 
            int(rt[6:8]), int(rt[8:10]))

def _dt_to_rt( dt ): 
    return dt.strftime( "%Y%m%d%H" )

def increment( rt, hours ): 
        dt = _rt_to_dt( rt )
        return _dt_to_rt( dt + datetime.timedelta( 0, 0, 0, 0, 0, int(hours), 0 ) )

def decrement( rt, hours ): 
        dt = _rt_to_dt( rt )
        return _dt_to_rt( dt - datetime.timedelta( 0, 0, 0, 0, 0, int(hours), 0 ) )

def diff_hours( rt2, rt1 ):
    # rt2 - rt1 in hours
    dt2 = _rt_to_dt( rt2 )
    dt1 = _rt_to_dt( rt1 )

    delta = dt2 - dt1

    if delta.microseconds != 0:
        print "WARNING: cycle_time.difference_hours(): unexpected timedelta"

    return delta.days * 24 + delta.seconds/3600

def is_valid( rt ):
    if re.compile( "^\d{10}$" ).match( rt ):
        try:
            _rt_to_dt( rt )
        except ValueError, x:
            print x
            return False

        return True
    else:
        return False
