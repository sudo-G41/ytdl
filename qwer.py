from src import ytdl
from time import strftime, localtime

a = strftime('%Y. %m. %d. %H:%M:%S(%a) KST')
print(a, type(a))

# ytdl.download_audio_only("https://youtu.be/CupFQnoO_28")

# a = None
# print("Y" if a else "n")