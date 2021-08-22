from datetime import datetime, timedelta

# ANSI colors
colors = (
    "\033[0m",   # End of color
    "\033[32m",  # Green
    "\033[31m",  # Red
    "\033[34m",  # Blue
    "\033[36m",  # Cyan
    "\033[35m",  # Magenta
    "\033[1m",   # Bold
    "\033[4m",   # Underline
)


def get_month_dates(any_date):
    default_date = datetime.strptime(any_date, '%Y-%m-%d') if any_date else datetime.now().date()
    year = default_date.year
    month = default_date.month
    next_month = default_date.replace(day=28) + timedelta(days=4)
    first_day = datetime(year, month, 1).date().strftime('%Y-%m-%d')
    last_day = (next_month - timedelta(days=next_month.day)).strftime('%Y-%m-%d')
    today = default_date.strftime('%Y-%m-%d')
    return today, first_day, last_day
