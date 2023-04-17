
from collections import namedtuple
from datetime import datetime
from os import stat
from os.path import dirname, isfile
from json import dumps, loads
from glob import glob
import pathlib

from . import google_calendar

FileStats = namedtuple("FileStats", "path stats")

def main(**args):
    if isfile(args["userCalendarCacheFile"]):
        print("Loading events from file")
        events = loads( open(args["userCalendarCacheFile"]).read() )
    else:
        print("Loading events from Google Calendar")
        events = google_calendar.get_events(
            args["secrets"], args["calendarId"], args["startDate"], args["endDate"]
        )
        
        try:
            pathlib.Path( dirname(args["userCalendarCacheFile"]) ).mkdir(parents=True, exist_ok=True)
            with open(args["userCalendarCacheFile"], "w") as user_calendar_cache_file:
                user_calendar_cache_file.write(dumps(events, indent=4, default=str))
        except Exception as e:
            print(e)
            raise
    
    # TODO #1 Refactor to be used by other modules
    files_to_process = [
        FileStats(file, stat(file))
        for directory in args["file_filters"]
        for file in glob( str(pathlib.Path(directory).expanduser()) )
    ]
    files_to_process.sort(key=lambda file_info: file_info.stats.st_mtime)
    events_with_files = [
        {
            "id": event["id"], 
            "start": event["start"]["dateTime"], 
            "end": event["end"]["dateTime"], 
            "summary": event["summary"], 
            "files": [file
                for file in files_to_process
                if (
                    datetime.fromisoformat(event["start"]["dateTime"])
                    <= datetime.fromtimestamp(file.stats.st_mtime).astimezone()
                    < datetime.fromisoformat(event["end"]["dateTime"])
                )
            ], 
        }
        for event in events
    ]

    def get_path_components(path):
        path = pathlib.Path(path)
        basedir = str(path.parent)
        basename = path.name
        return basedir, basename
    file_actions = [
        {
            "path": file.path,
            "actions": [
                (
                    "rename", 
                    args["substitutionString"]
                        .replace("$dirname", get_path_components(file.path)[0])
                        .replace("$summary", event["summary"])
                        .replace("$basename", get_path_components(file.path)[1])
                )
            ],
        }
        for event in events_with_files
        for file in event["files"]
    ]

    print("Loaded %d events" % len(events))
    return { "events_with_files": events_with_files, "file_actions": file_actions }
