#!/usr/bin/env python
import csv
import os

DEFAULT_INPUT_FILENAME = "data/test.csv"
DEFAULT_FILE_MAX_LINE = 5000
DEFAULT_OUTPUT_FILENAME_START_NUMBER = 1

# input filename
input_filename = input("请将要分割的文件拖动到窗口范围内。")
if len(input_filename) < 1:
    input_filename = DEFAULT_INPUT_FILENAME

# max line of output file
max_line = input("请输入分割后每个文件最大行数（默认%s行）：" % DEFAULT_FILE_MAX_LINE)
if len(max_line) < 1:
    max_line = DEFAULT_FILE_MAX_LINE
max_line = int(max_line)

# output directory
working_directory = os.path.dirname(input_filename)


# output filename
def get_output_filename(input_filename, number):
    filename, ext = os.path.basename(input_filename).split('.')
    output_filename = filename + str(number) + '.' + ext
    return os.path.join(working_directory, output_filename)


with open(input_filename, 'r', newline='') as inputcsv:
    reader = csv.reader(inputcsv)
    number = DEFAULT_OUTPUT_FILENAME_START_NUMBER
    output_filename = get_output_filename(input_filename, number)
    output_file = open(output_filename, 'w', newline='')
    writer = csv.writer(output_file)
    for row in reader:
        # title line
        if reader.line_num == 1:
            title = row
            writer.writerow(title)
            continue

        # truncate
        if (reader.line_num - 1) % max_line == 0:
            number += 1
            output_file.close()
            output_filename = get_output_filename(input_filename, number)
            output_file = open(output_filename, 'w', newline='')
            writer = csv.writer(output_file)
            writer.writerow(title)

        # copy line
        print("%d - %s" % (reader.line_num, output_filename))
        writer.writerow(row)
    output_file.close()
