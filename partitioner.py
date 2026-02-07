def partition(filesize:int, primary_parts:int):
   if filesize >= 104857600: #100MB
      partsize = filesize // primary_parts
      last_partsize = filesize - partsize * primary_parts
      total_parts = primary_parts + (0 if last_partsize == 0 else 1) 

      file_parts = []
      for part in range(1, total_parts + 1):
         part_info = {
            "part": part,
            "partname": f"SampleName.ext.temp{part}",
            "start_byte": (part - 1) * partsize,
            "end_byte": (part * partsize - 1) if part < total_parts else filesize - 1
         }
         file_parts.append(part_info)
      return {
         "filesize": filesize,
         "partition_data": file_parts
      }
   else: return {
      "filesize": filesize,
      "partition_data": [{
         "part": 1,
         "partname": f"SampleName.ext.temp1",
         "start_byte": 0,
         "end_byte": filesize - 1
      }]
   }