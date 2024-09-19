from datetime import datetime
from zoneinfo import ZoneInfo
import os

os.environ["TZ"] ="Asia/Ho_Chi_Minh"
date = datetime.now()

print(date)