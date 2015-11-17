#!/bin/bash

grep 'c:\|0x3\|0x7\|0x8\|Full Path Filename' all_libraries.txt > all_libraries_trimmed.txt
python exe_identify_txt_to_csv.py
sed -e "s///g" all_libraries.csv > t1
cat t1 | sort | uniq | sed "s/0x8 =>//" | sed "s/0x3 =>//" | sed "s/0x7 =>//" > All_Libraries_Final.csv
sed -i '1s/^/Full Path Filename, File Version , Product Name, Parent Product\n/' All_Libraries_Final.csv
