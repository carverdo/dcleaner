## Getting Started / Overall instructions
0. Create local version of project by taking from github.
1. create your own venv directory (won't be in github) and import any package requirements;
2. Adjust app.db_models to the model you want to work with;
3. Name the database in config.py / via environment vars;
4. Physically create database in pgadmin;
5. Move (db_create_migrate.py OR manager.py and) db_init_data.py underneath src root;
6. run these via cmd window to establish database model in pgadmin;
7. tailor views.py as you need to.
8. run run.py.


## Included (non-standard) Directories
*one_offs* Create a one_offs directory (for stuff used in set up only say).
`db_create_migrate` and `_init_data` fit well here.

*del_area* Temporary trash can. This will have its own gitignore to ignore_all in that subdirectory.

*logs, migrations, tests* fairly self-explanatory.

*venv*
`File / Settings / Project Interpreter / Create VirtualEnv` - put venv subdirectory immediately beneath src root.
Managing the venv is now a lot easier - we can import any package:
`File / Settings / Project Interpreter / Plus Sign`

Note that `psycopg2` (for some reason) still has problems with importing (we saw it earlier pre-pycharm and same here);
Just copy across from Python27/lib/site-packages to venv/lib/site-packages.

`requirements.txt`: place beneath src root - tells the current interpreter (our venv) that it should contain
these packages making their update simple (just open a .py and look at banner top).
Just edit the pre-populated one supplied to suit.
(This file works with heroku also.)


## Non-directory / Immediate Files  
*config.py and variants* primarily for DB setting;  
don't forget to input the local database via the environment vars;
 look to `config_vars`

*app/init* and *run.py*
 ` __init__` for app and db creation; and
 these are auto-run when called by `run.py`

*manager.py*
 sets up commands for you to use cmd directly.

*requirements.txt*
 see *venv*

*procfile*
 see *heroku*


## app  
Contains static and templates (see below)... more to follow.


## Templates and static/css  
`layout` is the template for all other templates.
 calls in all sorts of external fonts, bootstrap, highcharts etc.
 look to static/css.  
also calls `main_new.css` - our modifications to those imported themes.
 each (sub-)template extends layout and then calls its main blocks -
- redder (calls input_errors); and
- content.

`macros` knows how to:
- present forms (around which panels are drawn); 
- present panels; and 
- present rows (within panels).

the `tdata.htmls` supply the data to those rows;
 panel header info supplied via `views.py / patex`


# Pycharm 
## Local Set Up
`Run / Edit Config / Defaults / Python / Command Line` -
 so we can play with scripts after running.  
`File / Settings / Project Structure / Source` - set up as source directory.


# Heroku
Place procfile beneath src root - specific instructions to heroku.
 Edit the pre-populated file supplied.


# Git
## Gitignores
Create gitignore directly beneath src root.
 Use the intellij default and then tailor to, among other things, ignore the venv.
 This will keep the github sync as small as possible.
 (Place other gitignores under subdirectories as required.)