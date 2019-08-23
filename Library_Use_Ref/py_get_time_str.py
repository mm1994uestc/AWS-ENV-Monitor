import os 
import time 
import sys

def Get_time_str(separator,struct=''):
    if struct == '':
        time_struct_val = time.localtime(time.time())
        return str(time_struct_val.tm_year) + separator + str(time_struct_val.tm_mon) + separator + str(time_struct_val.tm_mday)+ separator + str(time_struct_val.tm_hour) + separator + str(time_struct_val.tm_min) + separator + str(time_struct_val.tm_sec)
    return str(struct.tm_year) + separator + str(struct.tm_mon) + separator + str(struct.tm_mday)+ separator + str(struct.tm_hour) + separator + str(struct.tm_min) + separator + str(struct.tm_sec)

print Get_time_str('-')
