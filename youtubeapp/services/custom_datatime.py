from datetime import datetime
from datetime import timedelta
        
def transform_datetime(publish_time):
    publish_time = datetime.strptime(publish_time, "%Y-%m-%dT%H:%M:%SZ")
    publish_time += timedelta(hours=9)
    return publish_time