
# Architecture
- Main script
    - Loads config.
    - Invokes modules.
    - After modules run, applies changes
- Module
    - Each gets 
        - a list of files to rename
        - rules to apply
        - additional data
    - A module may retrieve any additional data it may need.
    - Its output is 
        - a list of paths to perform actions on
        - Other additional data
