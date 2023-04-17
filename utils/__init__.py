
from collections import namedtuple
from glob import glob
from os import stat
from pathlib import Path


FileStats = namedtuple("FileStats", "path stats")

def glob_files(globs):
    return [
        FileStats(file, stat(file))
        for directory in globs
        for file in glob( str(Path(directory).expanduser()) )
    ]
