
from collections import namedtuple
from os import stat
from glob2 import glob
from pathlib import Path


FileStats = namedtuple("FileStats", "path stats")

def main(**args):
    # TODO #1
    files_to_process = [
        FileStats(str(file), stat(file))
        for directory in args["Actions"]
        for file in glob( str(Path(directory["Filter"]).expanduser()) )
        # TODO #2 Implement globbing with regexp
    ]
    files_to_process.sort(key=lambda file_info: file_info.stats.st_mtime)

    file_actions = [
        {
            "path": file.path,
            "actions": [
                (
                    (filter["Action"],)
                )
            ],
        }
        # TODO Handle deletions, moves, copies and linking
        # TODO When actiosn delete a file or rename it, throw appropriate exception.
        for filter in args["Actions"]
        for file in files_to_process
    ]

    return { "file_actions": file_actions }


