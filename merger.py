def merge_files(files:list, merged_path:str):

   rw_size = 10 * 1024 * 1024  # 10 MB read and write

   with open(merged_path, "wb") as merged:
      print("Merging files...")
      for part in files:
         with open(part, "rb") as f:
            while True:
               chunk = f.read(rw_size)
               if not chunk: break
               merged.write(chunk)

   print("Merging completed!")