__author__ = 'jfwright'


#f_read = open('/home/jfwright/Documents/all_libraries_trimmed.txt', 'r')
f_write = open('/home/jfwright/Documents/all_libraries.csv', 'w')
#f_write_2 = open('/home/jfwright/Documents/all_libraries_newline_fix.csv', 'w')

f_write.write("Full Path Filename, File Version , Product Name, Parent Product")

with open('/home/jfwright/Documents/all_libraries_trimmed.txt', 'r') as f_read:
    for each in f_read:
        if "c:" in each:
            f_write.write("\n" + each.strip("\n").replace(",",""))
        elif "0x3" in each:
            f_write.write("," + each.strip("\n").replace(",",""))
        elif "0x7" in each:
            f_write.write("," + each.strip("\n").replace(",",""))
        elif "0x8" in each:
            f_write.write("," + each.strip("\n").replace(",",""))
        else:
            continue

#with open("/home/jfwright/Documents/all_libraries.csv", 'r') as f_csv_read:
#    for each in f_csv_read:
##        if "c:" in each:
#            f_write_2.write(each)
#        else:
#            f_write_2.write(each.strip("\n"))

f_read.close()
f_write.close()
#f_write_2.close()
