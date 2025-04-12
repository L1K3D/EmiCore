from datetime import time, timedelta, timezone, datetime, date

def get_time():
    
    local_date = datetime.now()
    local_date = local_date.strftime("%Y-%m-%d | %H:%M:%S")
    
    return local_date