def partition_by_parts(filesize:int, primary_parts:int):
   if filesize >= 104857600: #100MB
      partsize = filesize // primary_parts
      last_partsize = filesize - partsize * primary_parts
      total_parts = primary_parts + (0 if last_partsize == 0 else 1) 
      print(f"Total {total_parts} parts")
      file_parts = []
      for part in range(1, total_parts + 1):
         start_end = (part - 1) * partsize, (part * partsize - 1) if part < total_parts else filesize - 1
         file_parts.append(start_end)
      return file_parts
   else:
      print("1 single part")
      return (0, filesize-1)
   
def partition_by_size(filesize:int, part_size:int):
   if filesize >= part_size: #100MB
      if filesize // part_size > 15:
         raise Exception("Too many parts, download will fail")
      
      else:
         total_parts = (filesize // part_size) + bool(filesize%part_size)
         print(f"Total {total_parts} parts")
         file_parts = []
         for part in range(1, total_parts + 1):
            start_end = (part - 1) * part_size, (part * part_size - 1) if part < total_parts else filesize - 1
            file_parts.append(start_end)
         return file_parts
         
   else:
      print("1 single part")
      return [(0, filesize-1)]
