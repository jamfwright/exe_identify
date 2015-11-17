# exe_identify

The main purpose of this is to recursively run through a specified directory (on Windows),
identify all EXE and DLL files, then extract the file path, file version, associated product,
and parent product.  This is all done with exe_identify.py.  Output is a text file.  Setting 
the directory to search is done within the script.

The other two scripts will parse the output (on Linux) to a CSV file.  Put the resulting txt 
file into the same directory as exe_identify_parse_results.sh and exe_identify_txt_to_csv.py
and execute the bash script exe_identify_parse_results.sh.


Known Issues

There are problems with the path output, some of the / are missing.

I find it kind of silly to have to move the txt output to a Linux box to parse to a CSV, but
there was little time to finesse.  If I can get back to this I'll fix the path display, and
make a fully native Python parser so that it can also be run on Windows.
