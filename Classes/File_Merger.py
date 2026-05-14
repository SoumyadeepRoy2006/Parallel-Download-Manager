from os import remove

class MergeJob:
   merged_file_name:str
   merge_dir:str
   part_list:list[str]
   
   rw_size = 2 * 1024**2 # MB
   
   total_size_bytes:int
   written_size_bytes = 0

   bridge = None

   def __init__(this, merge_dir:str, merged_file_name:str, total_parts:int, total_size_bytes:int):
      this.merged_file_name = merged_file_name
      this.merge_dir = merge_dir
      this.part_list = list[str]([None for i in range(total_parts)])
      this.total_size_bytes = total_size_bytes


   def set_bridge(this, bridge):
      this.bridge = bridge


   def add_part(this, part_no:int, part_full_path:str):
      if not part_no >= 1:
         raise ValueError("Part SlNo. cannot be less than 1")
      else:
         this.part_list[part_no-1] = part_full_path


   def check_ok(this):
      for i in this.part_list:
         if not i:
            return False
      return True


   def start(this):
      with open(f"{this.merge_dir}/{this.merged_file_name}", "wb") as merged_file:
         this.bridge.set_merge_status("start")
         print("Merging files...")
         for part_full_path in this.part_list:
            with open(part_full_path, "rb") as f:
               while True:
                  buffer = f.read(this.rw_size)
                  if not buffer: break
                  merged_file.write(buffer)
                  this.written_size_bytes += len(buffer)
                  this.bridge.set_merge_progress(this.written_size_bytes/this.total_size_bytes)
         this.bridge.set_merge_status("deleting_parts")
         for part_full_path in this.part_list:
            remove(part_full_path)
      this.bridge.set_merge_status("end")
      print("Merging completed!")
