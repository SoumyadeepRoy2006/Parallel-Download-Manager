import os, requests
from urllib.parse import urlparse

def get_download_info(url:str, timeout:int=10):
   result = {
      "file_name": None,
      "file_size_bytes": "UNKNOWN",
      "accept_ranges": False,
      "url": str(url)
   }

   headers = requests.head(url, allow_redirects=True, timeout=timeout).headers

   content_disposition = headers.get("Content-Disposition")
   if content_disposition:
      index = content_disposition.find("file_name=")
      result["file_name"] = content_disposition[index+9:].split("\"")[1]
   else:
      result["file_name"] = os.path.basename(urlparse(url).path)

   if headers["Content-Length"]:
      result["file_size_bytes"] = int(headers["Content-Length"])
   
   result["accept_ranges"] = headers["Accept-Ranges"] == "bytes"

   return result