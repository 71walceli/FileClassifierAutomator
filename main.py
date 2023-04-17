
from argparse import ArgumentParser
from importlib import import_module
from json import dumps as json_dumps
from glob import glob
from os import walk, stat
from pathlib import Path
import yaml


if __name__ == "__main__":
    tasks = []
    parser = ArgumentParser(
        description='help classify files and folders based on its attributes and external cata'
    )
    parser.add_argument("-c", '--config', required=True, metavar="<config>",
        help='Config file with specified medules.'
    )
    args = vars(parser.parse_args())
    try:
        with open(args["config"], "r") as config_file:
            tasks = yaml.load(config_file.read(), yaml.Loader)
            # TODO https://stackoverflow.com/a/22238613/20054027
        if len(tasks) == 0:
            print(f"ERROR: File {args['config']} has no valid configs")
    except FileNotFoundError:
        print(f"ERROR: File {args['config']} not found")
        exit(1)

    modules_results = {}
    for name, task in tasks.items():
        task_file_filters = task.get("FileFilters", [])
        for module, settings in task["Modules"].items():
            if settings is None:
                settings = dict()
            module_file_filters = task_file_filters + settings.get("FileFilters", [])
            modules_results[module] = import_module(f"{module}").main(
                file_filters=module_file_filters, **settings
            )
            if modules_results[module] is None:
                modules_results[module] = dict()

    for module, result in modules_results.items():
        for file in result.get("file_actions", []):
            for file_action in file["actions"]:
                # TODO Export to module
                try:
                    if file_action[0] == "rename":
                        path = Path(file["path"])
                        destination = Path(file_action[1])
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        path.rename(destination)
                        break
                    elif file_action[0] == "delete":
                        Path(file["path"]).unlink()
                        break
                except Exception as e:
                    # TODO Save mapping of errors to actions
                    print(f"ERROR: {e}")

