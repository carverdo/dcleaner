## Getting Started / Overall instructions
0. Create local version of project by taking from github.
1. create your own venv directory (won't be in github) and import any package requirements;

2. Adjust app.db_models to the model you want to work with;
3. Name the database in config.py / via environment vars;
4. Physically create database in pgadmin;
5. Move (db_create_migrate.py OR manager.py and) db_init_data.py underneath src root;
6. run these via cmd window to establish database model in pgadmin;

7. build out main2 so that you have project-specific `forms` and `views`.
8. run run.py.


## Directories outside of app
`del_area` Temporary trash can. This will have its own gitignore to ignore_all
 in that subdirectory.

`logs, migrations, tests` fairly self-explanatory.

`one_offs` Create a one_offs directory (for stuff used in set up only say).
`db_create_migrate` and `_init_data` fit well here.

`tests` empty.

`venv`
`File / Settings / Project Interpreter / Create VirtualEnv` - put venv subdirectory
 immediately beneath src root. Managing the venv is now a lot easier - we can import
 any package: `File / Settings / Project Interpreter / Plus Sign`

Note that `psycopg2` (for some reason) still has problems with importing (we saw it
earlier pre-pycharm and same here). Just copy across from Python27/lib/site-packages 
to `venv/lib/site-packages`.

`requirements.txt`: place beneath src root - tells the current interpreter (our venv)
that it should contain these packages making their update simple (just open a .py and
look at banner top). Just edit the pre-populated one supplied to suit.
(This file works with heroku also.)

## Files outside of app  
`config.py and variants` primarily for DB setting;  
don't forget to input the local database via the environment vars;
look to `config_vars`

`manager.py`
sets up commands for you to use cmd directly. run from cmd.

`procfile`
see `heroku`

`requirements.txt`
see `venv`

`run.py`
creates the app (heavily calling on `app\__init__`)

## app
there are two main blueprint areas: `main` and `main2` each of which gets paired
with the app as part of create_app.

`main` holds a user login system (since every project will need something similar).
`main2` is empty, waiting to be populated for each user-case. Contains static and 
templates (see below)... more to follow.

`templates and static/css` -  
`base.html` is the template for all other templates (dont change this name - jinja uses).
calls in all sorts of external fonts, bootstrap, highcharts etc. look to static/css.
also calls `main_new.css` - our modifications to those imported themes. each (sub-)template
extends layout and then calls its main blocks -
- redder (calls input_errors); and
- content.

`macros` knows how to:
- present forms (around which panels are drawn); 
- present panels; and 
- present rows (within panels).

the `tdata.htmls` supply the data to those rows; panel header info supplied via
`views.py / patex`

`db_models` for all model tailoring. 


# Pycharm 
## Local Set Up
`Run / Edit Config / Defaults / Python / Command Line` -
 so we can play with scripts after running.  
`File / Settings / Project Structure / Source` - set up as source directory.


# Git
## Gitignores
Create gitignore directly beneath src root. Use the intellij default and then tailor to,
among other things, ignore the venv. This will keep the github sync as small as possible. 
(Place other gitignores under subdirectories as required.)


# Heroku
Place procfile beneath src root - specific instructions to heroku.
Login via website, create and name a new app (make it snappy - it's public!)
Go to Deploy and connect to GitHub... you're (halfway) done!
Website will show up but it's a dummy: you won't be able to log-in. 

## Databases
...you still don't have a database.
### Provision a database
`Resources / Add-ons`: just type postgres in the box and click/select 
`Heroku Postgres Hobby-Dev Free` Provision.
### Promote
In git bash if we haven't already, `heroku login`.
`heroku addons` will show us that database.
`heroku pg:promote DATABASE` (which means rewire DATABASE; look to connection
setting `Psql` on the heroku dashboard). Not strictly necessary with only one db, but 
it will re-title the db with an easier-to-remember colour-scheme name.
### Copy across a DB
In pgAdmin right-click and `backup` to somewhere in dropbox. Copy the link which will look
like this:
`https://www.dropbox.com/s/8a2cmqr9hho96z3/gscore_v0.dump?dl=0`
But adjust (see start; drop the end):
`https://dl.dropboxusercontent.com/s/8a2cmqr9hho96z3/gscore_v0.dump`
And trick the system into using this back-up to 'restore' our database -
`heroku pg:backups restore ‘[DROPBOX LINK]’ [DATABASE] --app [APP NAME]` (keep the quotation
marks; rid squares, use real link, real database name)
Will get a destruction warning...
Quick-check: heroku dashboard should now show correct number of tables.

## Config Vars (under Settings)
Add a SECRET_KEY (otherwise you end up with lots of CSRF errors as heroku keeps regenerating);
no need for quotation marks as you enter the number.

Finito!