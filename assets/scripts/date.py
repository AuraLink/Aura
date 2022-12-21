import datetime
from assets.scripts.terminal import colors as tc

def now():
    return f"{tc.fg.darkgrey}\b{datetime.datetime.today().replace(microsecond=0)}"