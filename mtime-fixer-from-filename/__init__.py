from datetime import datetime
from os import stat, utime
import re
from dateutil import parser
from utils import FileStats, glob_files

DATE_REGEXP = r'(\d{4}).?(\d{2}).?(\d{2}).(\d{2}).?(\d{2}).?(\d{2})'

def try_parse_date_mtime(filename):
    try:
        # Extract the date string from the file name
        date_string = "".join(re.findall(DATE_REGEXP, filename)[0])
        # Parse the date string using dateutil module and create a datetime object
        date = parser.parse(date_string)
        # Format the datetime object to the desired output format
        return date.astimezone()
    except IndexError:
        return None

def main(**args):
    # TODO Manage in main module
    for file in glob_files(args["file_filters"]):
        mtime = try_parse_date_mtime(file.path)
        if mtime is not None:
            mtime = mtime.timestamp()
            atime = file.stats.st_atime
            utime(file.path, times=( atime, mtime ))

    


