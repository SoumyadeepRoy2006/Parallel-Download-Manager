import os, requests
from urllib.parse import urlparse

def extract_filename(url:int, headers:dict):
    cd = headers.get("Content-Disposition")
    if cd and "filename=" in cd:
        return cd.split("filename=")[-1].strip("\"'")
    return os.path.basename(urlparse(url).path) or "download.bin"

def get_info(url:str, timeout:int=10):
   result = {
      "url": str(url),
      "filename": None,
      "size": None,
      "accept_ranges": bool(False),
      "verified_ranges": bool(False),
      "best_mode": str("STREAM ONLY")
   }

   head = requests.head(url, allow_redirects=True, timeout=timeout); head.raise_for_status()
   
   headers = head.headers

   result["filename"] = str(extract_filename(url, headers))
   if "Content-Length" in headers: result["size"] = int(headers["Content-Length"])
   if headers.get("Accept-Ranges", "").lower() == "bytes": result["accept_ranges"] = True
   if result["size"] is not None:
      test_headers = {"Range": "bytes=0-0"}
      r = requests.get(url, headers=test_headers, stream=True, timeout=timeout)
      if r.status_code == 206: result["verified_ranges"] = True
   if result["size"] is not None:
      if result["verified_ranges"]: result["best_mode"] = "PARALLEL"
      else: result["best_mode"] = "SINGLE"
   
   return result