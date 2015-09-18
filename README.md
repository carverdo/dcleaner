## Getting Started / Overall instructions
0. Create local version of project by taking from github.
1. Create your own venv directory (won't be in github) and import any package requirements;
2. Adjust app.db_models to build the db model you want to work with;
3. Name the database in config.py / via environment vars;
4. Physically create database in pgadmin;
5. (Move (`db_create_migrate.py` OR `manager.py` and) `db_init_data.py` underneath src root;)
6. Run these via cmd window to establish database model in pgadmin;
7. Run `run.py`.
8. Now you're free to build out proj for project-specific `forms` and `views`.

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

`requirements.txt`: place beneath src root; tells the current interpreter (our venv)
that it should contain these packages making their update simple (just open a .py and
look at banner top). Just edit the pre-populated one supplied to suit.
(This file works with heroku also.)

## Files outside of app  
`config.py and variants` primarily for DB setting; don't forget to input the 
local database via the environment vars; look to `config_vars`

`manager.py` sets up commands for you to use cmd directly; run from cmd.

`procfile` see `heroku`.

`requirements.txt` see `venv`.

`run.py` creates the app (heavily calling on `app\__init__`).

## app
there are two main blueprint areas: `log_auth` and `proj` each of which gets paired
with the app as part of `create_app`.

`log_auth` holds a user login system (since every project will need something similar).
`proj` is empty, waiting to be populated for each user-case. Contains static and 
templates (see below)... more to follow.

`templates and static/css`  
`base.html` is the template for all other templates (dont change this name - jinja uses).
calls in all sorts of external fonts, bootstrap, highcharts etc. look to `static/css`.
also calls `main_new.css` - our modifications to those imported themes. each (sub-)template
extends layout and then calls its main blocks -
- redder (calls input_errors); and
- content.

`macros` knows how to:
- present forms (around which panels are drawn); 
- present panels; and 
- present rows (within panels).
etc.

the `tdata.htmls` supply the data to those rows; panel header info supplied via
`views.py / patex`

`db_models` for all model tailoring. 


# Pycharm / Local Set Up
`Run / Edit Config / Defaults / Python / Command Line` so we can play with scripts after running.  
`File / Settings / Project Structure / Source` - set as source directory.  

# Github (deploy part 1)
Make sure your new pycharm project is git-enabled.
## Gitignores
Create gitignore directly beneath src root. Use the intellij default and then tailor to,
among other things, ignore the venv. This will keep the github sync as small as possible. 
(Place other gitignores under subdirectories as required.)  
Make sure there are no stray files / folders, even .pycs. Clear the logs.

# Heroku (deploy part 2)
Make sure procfile is beneath src root - specific instructions to heroku. Double-check 
`requirements.txt`. Login via website, create and name a new app (make it snappy - it's 
a public url!). Go to Deploy and connect to GitHub... you're (halfway) done! Website will 
show up but it's a dummy: you won't be able to log-in.
 
## Error Checklist
1. set create_app('production') / debug=False?
2. tested on local AND production?
3. double-checked all config / environment vars (in production)?
4. got rid of stray files incl .pycs?
5. got rid of stray folders?
6. gitignores all ok?
7. procfile names all good?
8. requirements.txt correct?
9. git up to date?
10. double-checked that don't need any config / environ vars in heroku?
11. does the slug look too big (7MB about right)?

## Databases / Provision a database
You still don't have a database.
`Resources / Add-ons`: just type postgres in the box and click/select 
`Heroku Postgres Hobby-Dev Free` Provision.
### Promote
In git bash if we haven't already, `heroku login`.  
`heroku addons` will show us our databases.  
`heroku pg:promote DATABASE -app [NAME OF APP]` (which means rewire DATABASE; test this by looking to connection
setting `Psql` on the heroku dashboard). Not strictly necessary with only one db, but 
it will re-title the db with an easier-to-remember colour-scheme name.
### Capture Backup facility
`herok pg:backups capture --app [APP NAME]`: captures this facility, ie now you can use 'backups'.


### Copy across a DB
In pgAdmin right-click and `backup` to somewhere in dropbox. Copy the link which will look
like this:
`https://www.dropbox.com/s/8a2cmqr9hho96z3/gscore_v0.dump?dl=0`  
But adjust (see start; drop the end):
`https://dl.dropboxusercontent.com/s/8a2cmqr9hho96z3/gscore_v0.dump`  
And trick the system into using this back-up to 'restore' our database -
`heroku pg:backups restore ‘[DROPBOX LINK]’ [DATABASE] --app [APP NAME]` (keep the quotation
marks; rid squares, use real link, real database name eg HEROKU_POSTGRES_COPPER_URL)  
Will get a destruction warning...
Quick-check: heroku dashboard should now show correct number of tables.

## Config Vars (under Settings)
Add a `SECRET_KEY` (otherwise you end up with lots of CSRF errors as heroku keeps regenerating);
no need for quotation marks as you enter the number. Only need to do once per project.
Repeat for any other config vars set by environment.

## Debug = False
Don't forget.
Finito!