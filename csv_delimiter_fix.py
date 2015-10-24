""" 

Changes delimiter: ^ -> ,
For CSVs ending in .txt

"""

import sys, os, fnmatch

if not len(sys.argv) > 1:
    print 'Error: You must specify a directory'
    sys.exit(0)

directory = sys.argv[1]

if not os.path.isdir(directory):
    print 'Error: Not a valid directory'
    sys.exit(0)

# Create list of all TXT file locations
locations = []
for root, dirnames, filenames in os.walk(directory):
    for filename in fnmatch.filter(filenames, '*.txt'):
        locations.append(os.path.join(root, filename))

if not locations:
    print 'Error: No TXT files found in directory'
    sys.exit(0)

for location in locations:
    parent_dir = os.path.abspath(os.path.join(location, os.pardir))
    converted_dir = os.path.join(parent_dir, 'converted')

    # Create converted directory
    if not os.path.exists(converted_dir):
        os.makedirs(converted_dir)

    filename = os.path.basename(location)

    # Convert TXT
    print("Converting %s..." % location),

    csv_location = os.path.join(converted_dir, filename[:-4] + '.csv')

    if os.path.isfile(csv_location):
        print ' Already Converted!'
        continue

    with open(csv_location,'w') as new_file:
        with open(location) as old_file:
            for line in old_file:
                new_file.write(line.replace('^', ','))

    print ' Done!'
