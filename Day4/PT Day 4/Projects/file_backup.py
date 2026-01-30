import shutil
import datetime

source="Disc_usage.txt"

backup=f"backup_{datetime.date.today()}.txt"
shutil.copy(source,backup)
print("Back up created")