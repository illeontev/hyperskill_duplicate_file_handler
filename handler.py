import hashlib
import os
import sys

if len(sys.argv) <= 1:
   print("Directory is not specified")
   exit(0)

file_format = input("Enter file format:\n")

print("\nSize sorting options:\n"
      "1. Descending\n"
      "2. Ascending\n")

while True:
   sorting_option = input("Enter a sorting option:\n")
   if sorting_option not in ("1", "2"):
      print("Wrong option")
   else:
      break

cur_dir = sys.argv[1]
files_dict = {}
for root, dirs, files in os.walk(cur_dir, topdown = True):
   for name in files:
      ext = os.path.splitext(name)[1][1:]
      if ext == file_format or file_format == "":
         full_path = os.path.join(root, name)
         size = os.path.getsize(full_path)
         files_dict.setdefault(size, []).append(full_path)

if sorting_option == "1":
   rev = True
else:
   rev = False

for key in sorted(files_dict.keys(), reverse=rev):
   print(f"\n{key} bytes")
   for path in files_dict[key]:
      print(path)

while True:
   check_for_duplicates = input("\nCheck for duplicates?\n")
   if check_for_duplicates in ("yes", "no"):
      break

if check_for_duplicates == "yes":
   for num_of_bytes, list_of_files in files_dict.items():
      hash_dict1 = {}
      for filename in list_of_files:
         with open(filename, "rb") as f:
            data = f.read()
            hash_of_file = hashlib.md5(data)
            hash_dict1.setdefault(hash_of_file.hexdigest(), []).append(filename)
      files_dict[num_of_bytes] = hash_dict1

   duplicates = []
   count = 1
   for num_of_bytes in sorted(files_dict.keys(), reverse=rev):
      hash_dict = files_dict[num_of_bytes]
      print_bytes_info = False
      for hash_of_file, filenames in hash_dict.items():
         if len(filenames) > 1:
            print_bytes_info = True
            break

      if print_bytes_info:
         print(f"\n{num_of_bytes} bytes")
         for hash_of_file, filenames in hash_dict.items():
            if len(filenames) > 1:
               print(f"Hash: {hash_of_file}")
               for filename in filenames:
                  print(f"{count}. {filename}")
                  duplicates.append({count: {"filename": filename, "size": num_of_bytes}})
                  count += 1

   if duplicates:
      while True:
         delete_files = input("\nDelete files?\n")
         if delete_files not in ("yes", "no"):
            continue

         if delete_files == "no":
            exit(0)

         if delete_files == "yes":
            while True:
               try:
                  file_numbers_input = input("\nEnter file numbers to delete:\n")
                  if file_numbers_input == "exit":
                     exit()
                  file_numbers = [int(i) for i in file_numbers_input.split()]
                  file_found = False
                  # for file_number in file_numbers:
                  for duplicate in duplicates:
                     for key in duplicate:
                        if key in file_numbers:
                           file_found = True
                  if not file_found:
                     raise Exception
                  break
               except:
                  print("Wrong format")
                  continue

            sum_of_size = 0
            for duplicate in duplicates:
               for key, file_info in duplicate.items():
                  if key in file_numbers:
                     os.remove(file_info["filename"])
                     sum_of_size += file_info["size"]

            print(f"\nTotal freed up space: {sum_of_size} bytes")
            break



