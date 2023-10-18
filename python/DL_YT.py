
#%%
from yt_dlp import YoutubeDL
url = ""
with YoutubeDL() as ydl:
    result = ydl.download([url])