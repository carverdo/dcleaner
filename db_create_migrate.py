#!flask/bin/python
"""
Before running remember to physically create database using postgres!
(Make sure to close all connections / python scripts looking at database otherwise errors occur.)

Move this script directly beneath app (couldn't fix relative addressing)
RUN this script from the cmd line -

1. Create migrations folder
cd to the folder holding this file.
    C:..> venv\scripts\activate [HAS TO BE BACKSLASH!]
    <venv> C:..> python db_create_migrate.py db init
(it will say Please edit ... before proceding; this is not an error, just info.)

2. For EVERY model change (including the first model-overlay on blank dbase)
(each will flash INFO messages)

2a. Generate one empty table: [alembic_version]
     <venv> C:..> python db_create_migrate.py db migrate

2b. Generate all the other tables
    <venv> C:..> python db_create_migrate.py db upgrade
We can of course also run: > python db_create_migrate.py db downgrade

3. OPTIONAL (to populate) [can just do via normal python]
    <venv> C:..> python db_init_data.py init_data
"""

# =================
# import MANAGER
# and run (as is, no changes)
# manager.run() has the effect of freezing all changes in place
# =================
import manager
if __name__ == '__main__':
    manager.run()