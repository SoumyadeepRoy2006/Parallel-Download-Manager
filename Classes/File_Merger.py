from os import remove
class MergeJob:
   merged_file_name:str
   merge_dir:str
   part_list:list[str]
   rw_size = 100 * 1024 * 1024 # 100 MB

   def __init__(this, merge_dir:str, merged_file_name:str, total_parts:int):
      this.merged_file_name = merged_file_name
      this.merge_dir = merge_dir
      this.part_list = list[str]([None for i in range(total_parts)])

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
       # 100 MB read and write

      with open(f"{this.merge_dir}/{this.merged_file_name}", "wb") as merged_file:
         print("Merging files...")
         for part_full_path in this.part_list:
            with open(part_full_path, "rb") as f:
               while True:
                  buffer = f.read(this.rw_size)
                  if not buffer: break
                  merged_file.write(buffer)
            remove(part_full_path)

      print("Merging completed!")
