from info_check import get_info
from partitioner import partition
from downloader import download

PARTS = 5
URL = str(input("Link ->  ")) 

info = get_info(url=URL)

filename = info["filename"]
filesize = info["filesize"]
print(filename)
download_data = partition(filesize, PARTS)
print(f"{filesize/1024} KB" if filesize < 1024 * 1024 else f"{filesize/1024**2} MB")

if info["best_mode"] == "PARALLEL": download(url=URL, filename=filename, download_data=download_data)
