# Skeleton_Flask_v11

## Heading
# Big heading

*Italics*
**Bold**
**Some _bold and italic**
> Block quotes

- List
- List
- List

1. Item 1
2. Item 2

And I can indicate 'code sections' here.
Check out this neat program I wrote:

```
x = 0
x = 2 + 2
what is x
```

Hyperlinks with label -
[Visit GitHub!](https://www.github.com)


## Included (non-standard) Directories
*one_offs* Create a one_offs directory (for stuff used in set up only say).
`db_create_migrate` and `_init_data` fit well here.

*del_area* Temporary trash can. This will have its own gitignore to ignore_all in that subdirectory.

*logs, migrations, tests* fairly self-explanatory.

`app`
Contains static and templates...

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


## Non-directory Files
 *config.py and variants* primarily For DB setting;
don't forget to input the local database via the environment vars;
look to `config_vars`

*app/init* and *run.py*
` __init__` for app and db creation; and
 these are auto-run when called by `run.py`

*manager.py*
`manager.py` sets up commands for you to use cmd directly.

*requirements.txt*
see *venv*

*procfile*
see *heroku*


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

the `tdata.htmls` supply the data to those rows'
panel header info supplied via `views.py / patex`


# PYCHARM 
## Local Set Up
Run / Edit Config / Defaults / Python / Command Line - so we can play with scripts after running.
File / Settings / Project Structure / Source - set up as source directory.


# HEROKU
Place procfile beneath src root - specific instructions to heroku. Edit the pre-populated file supplied.


# GIT 
## GITIGNORES
Create gitignore directly beneath src root.
Use the intellij default and then tailor to, among other things, ignore the venv.
This will keep the github sync as small as possible.
(Place other gitignores under subdirectories as required.)

