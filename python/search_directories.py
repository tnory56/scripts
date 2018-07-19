#!/usr/bin/python
# title             :search_directories.py
# description       :Find strings within a directory recursively
# author            :Thomas Norberg
# date              :20180718
# version           :1.0.0
# usage             :python search_directories.py
# python_version    :2.6.6
# ==============================================================================

from os import listdir
from os.path import isfile, join, isdir
import re, base64

# Modify directories as needed
directories = [
    'mobileapp-android-master',
    'mobileapp-ios-master',
]

# Change to True to export to file
export_to_file = True
# Change to a different file name if you want
export_file_name = 'search_results.txt'
# Turn to True to show all responses from all files in a directory
# This might produce undesirable results
show_empty_responses = False
# Enable progress meter only when exporting to file
enable_progress_meter = False

# Optional settings
# Search string modification
search_strings = [
    # Pretty straight forward regex
    # Normal ones
    '(?P<url>https?:?/?/?[^\s]+)',
    'ftp:\/\/|www\.|https?:\/\/{1}[a-zA-Z0-9u00a1-\uffff0-]{2,}\.[a-zA-Z0-9u00a1-\uffff0-]{2,}\S*',
    # End normal ones
    # This one is a bit nutty, we get all sorts of garbage from the binary data files
    # '(?:(?:https?|ftp):\/\/|\b(?:[a-z\d]+\.))(?:(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))?\))+(?:\((?:[^\s()<>]+|(?:\(?:[^\s()<>]+\)))?\)|[^\s`!()\[\]{};:\'".,<>?]))?',
    # These base64 encoded regexes did not return anything but we include anyway
    # '(?P<url>' + base64.b64encode('https://') + '[^\s]+)',
    # '(?P<url>' + base64.b64encode('http://') + '[^\s]+)',
    # '(?P<url>' + base64.b64encode('https') + '[^\s]+)',
    # '(?P<url>' + base64.b64encode('http') + '[^\s]+)',
    # '(?P<pword>password[^\s]+)',
    # base64.b64encode('password'),
]

# DO NOT EDIT BELOW THIS LINE #
just_results = []
output_contents = []

textchars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))

file_count = 0
directory_count = 0
file_count_inc = 0
directory_count_inc = 0


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    print '\r[%s] %s%s ...%s\r' % (bar, percents, '%', status)


def return_results(search_term, the_file):
    results = []
    for line in the_file:
        the_results = re.findall(search_term, line, re.IGNORECASE)
        if the_results.__len__() > 0 and show_empty_responses is False:
            results.append(the_results)
        elif show_empty_responses is True:
            results.append(the_results)
    return results


def search_file(file_name, search_term):
    the_file = open(file_name, "rb")
    if is_binary_string(the_file.read(1024)):
        results = return_results(search_term, the_file)
        the_file.close()
    else:
        new_file = open(file_name, "r")
        results = return_results(search_term, new_file)
        new_file.close()
    if results.__len__() > 0 and show_empty_responses is False:
        return results
    elif show_empty_responses:
        return results
    else:
        return False


def get_files(the_path):
    return listdir(the_path)


def get_file_counts(the_path):
    global file_count, directory_count
    files = listdir(the_path)
    for filename in files:
        full_path = join(the_path, filename)
        if isfile(full_path):
            file_count += 1
        elif isdir(full_path):
            directory_count += 1
            get_file_counts(full_path)
        else:
            # Fail safe to find anything else
            print filename


def search_files(the_path):
    global file_count_inc, directory_count_inc
    for filename in get_files(the_path):
        full_path = join(the_path, filename)
        if isfile(full_path):
            file_count_inc += 1
            for search_string in search_strings:
                contents = search_file(full_path, search_string)
                if contents:
                    populate_contents(contents, full_path, filename, search_string)
        elif isdir(full_path):
            directory_count_inc += 1
            search_files(full_path)
    if enable_progress_meter:
        progress(file_count_inc, file_count,
                 status="Files completed %d/%d Found Items: %d" % (file_count_inc, file_count, just_results.__len__()))


def populate_contents(contents, full_path, filename, search_string):
    output_data = [
        "Search String: %s" % search_string,
        "Directory Count: %d" % directory_count_inc,
        "File Count: %d" % file_count_inc,
        "Full Path: %s" % full_path,
        "File name: %s" % filename,
        "Data Found:"
    ]
    for data in contents:
        for content in data:
            # maybe move formatting to other part
            just_results.append("\t" + content)
            output_data.append("\t" + content)
    output_data.append("\n")

    for output in output_data:
        if export_to_file:
            output_contents.append(output)
        else:
            # This is so we can see the results right away
            print output


def run():
    print "Gathering data..........."
    for directory in directories:
        get_file_counts(directory)
    for directory in directories:
        search_files(directory)

    the_results = sorted(list(set(just_results)))
    total_item_count = just_results.__len__()
    unique_item_count = the_results.__len__()
    directory_string = ("this directory", "these directories")[directories.__len__() > 1]
    status_top = "\nFrom %s:\n%s\nHere are the search results (Duplicates Removed):\n\n#START_RESULTS#" \
                 % (directory_string, "\n".join(directories))
    status_bottom = "#END_RESULTS#\n\nDirectories Scanned: %s/%s\nFiles Scanned: %s/%s\n" \
                    % (str(directory_count_inc), str(directory_count), str(file_count_inc), str(file_count))
    status_bottom += "Total item count: %d\nUnique total item count: %d" \
                     "\n\n######COMPLETE######\n\nNOTE: Search for #START_RESULTS# " \
                     "To find the beginning of the search results" % (total_item_count, unique_item_count)

    output_contents.append(status_top)
    for result in the_results:
        output_contents.append(result)
    output_contents.append(status_bottom)
    if export_to_file:
        with open(export_file_name, 'a') as export_file:
            export_file.truncate()
            export_file.write("\n".join(output_contents))
    print status_top
    print "\n".join(the_results)
    print status_bottom


run()
