#!/bin/bash

# Go to the correct directory that contains the shell file
cd "$(dirname "$0")"

# Generate the dirty data
python3 generate_dirty_data.py

# Remove ms_data.csv first to make sure this script doesn't run multiple times for incorrect results
rm "ms_data.csv"

# Piping grep, awk, and cut together to pipe three commands together
# grep removes empty lines and lines with #
# awk goes line by line to remove the excessive commas
# cut extracts the columns we want
# redirect the output to the ms_data.csv instead of the terminal
grep -v -E '^\s*$|^\s*#' ms_data_dirty.csv | awk -F, '{
    for (i = 1; i <= NF; i++) {
        if ($i != "") {
            if(i == NF){
                printf ("%s\n", $i);
            }else{
                printf ("%s,", $i);
            }
            
        }
    }
}' | cut -f 1,2,4,5,6 -d ','> ms_data.csv

# create a new file named insrance.lst to store the insurance types
# Delete file first to ensure no duplication in case someone run this file multiple times
rm "insurance.lst"
echo "Basic" >> insurance.lst
echo "Premium" >> insurance.lst
echo "Platinum" >> insurance.lst
echo "Deluxe_Premium" >> insurance.lst
echo "Ultimate" >> insurance.lst

# Store number of lines into a variable then -1 to exclude the header
# Print out the number of visits, and display the first 10 visits
n_line=$(($(wc -l < ms_data.csv) -1)) 
echo ""
echo "------Summary of the Processed Data:------"
echo "there are $n_line visits/rows in the data(not including the headers)"
echo ""
echo "------First 10 Visits:------"
tail -n +1 ms_data.csv | head -10