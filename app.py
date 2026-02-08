from pprint import pprint
from info_check import get_info
from partitioner import partition
from downloader import download

PARTS = 5
URL = "https://mirror.freedif.org/zorin/18/Zorin-OS-18-Core-64-bit-r3.iso" 

info = get_info(url=URL)

filename = info["filename"]
filesize = info["filesize"]
print(filename)
download_data = partition(filesize, PARTS)
print(f"{filesize/1024} KB" if filesize < 1024 * 1024 else f"{filesize/1024**2} MB")

if info["best_mode"] == "PARALLEL": download(url=URL, filename=filename, download_data=download_data)
