from datetime import datetime, timedelta

# Task 1
current_date = datetime.today()
five_days_ago = current_date - timedelta(days=5)
print("Five days ago:", five_days_ago.strftime("%Y-%m-%d"))

# Task 2
yesterday = current_date - timedelta(days=1)
tomorrow = current_date + timedelta(days=1)

print("Yesterday:", yesterday.strftime("%Y-%m-%d"))
print("Today:", current_date.strftime("%Y-%m-%d"))
print("Tomorrow:", tomorrow.strftime("%Y-%m-%d"))

# Task 3
without_microsec = current_date.replace(microsecond=0)
print("Current datetime without microseconds:", without_microsec)

# Task 4
date1 = datetime(2025, 2, 10, 12, 0, 0)
date2 = datetime(2025, 2, 14, 15, 30, 0)

difference_in_seconds = abs((date2 - date1).total_seconds())
print("Difference between two dates in seconds:", difference_in_seconds)
