""" 

Recursively converts all DBF files in a directory to CSV.
Puts all CSV files in a "converted" directory in the same
directory as the DBF file. Does not delete or modify DBF
files.

Note: Microsoft Office Excel must be installed.
Install http://sourceforge.net/projects/pywin32/ to use.

Example use:
convert.py "C:\dbf_files"

"""

import sys, os, fnmatch, win32com.client as win32

if not len(sys.argv) > 1:
    print 'Error: You must specify a directory'
    sys.exit(0)

directory = sys.argv[1]

if not os.path.isdir(directory):
    print 'Error: Not a valid directory'
    sys.exit(0)

# Create list of all DBF file locations
locations = []
for root, dirnames, filenames in os.walk(directory):
    for filename in fnmatch.filter(filenames, '*.DBF'):
        locations.append(os.path.join(root, filename))

if not locations:
    print 'Error: No DBF files found in directory'
    sys.exit(0)

for location in locations:
    parent_dir = os.path.abspath(os.path.join(location, os.pardir))
    converted_dir = os.path.join(parent_dir, 'converted')

    # Create converted directory
    if not os.path.exists(converted_dir):
        os.makedirs(converted_dir)

    filename = os.path.basename(location)

    # Convert DBF
    print("Converting %s..." % location),

    csv_location = os.path.join(converted_dir, filename[:-4] + '.csv')

    if os.path.isfile(csv_location):
        print ' Already Converted!'
        continue

    # Convert with Microsoft Office Excel
    # Open Office unoconv can be substituted
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    book = excel.Workbooks.Open(location)

    # SaveAs File Formats: 
    # https://msdn.microsoft.com/en-us/library/office/ff198017.aspx
    book.SaveAs(csv_location, 6)
    book.Close(False)

    print ' Done!'
