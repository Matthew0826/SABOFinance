from datetime import datetime
import pytz

# Set the timezone
est = pytz.timezone('America/New_York')

# Get the current time
def get_time():
    return datetime.now(pytz.UTC).astimezone(est)

# Print the current time (or get in a string format)
def time_to_string( time:datetime ):
    return time.strftime('%Y-%m-%d %H:%M:%S')

# Get the elapsed time (in seconds)
def get_delta_time( startTime:datetime, endTime:datetime ):
    return (startTime - endTime).total_seconds()


