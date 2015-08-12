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


## Templates and CSS
`layout` is the template for all other templates.
calls in all sorts of external fonts, bootstrap, highcharts etc.
look to static/css
also calls `main_new.css` - our modifications to those imported themes.
each (sub-)template extends layout and then calls its main blocks - 
- redder (calls input_errors); and
- content.

macros knows how to: 
- present forms (around which panels are drawn); 
- present panels; and 
- present rows (within panels).

the `tdata.htmls` supply the data to those rows'
panel header info supplied via `views.py / patex`


## Included Directories
*ONE_OFFS* Create a one_offs directory (for stuff used in set up only say).
`db_create_migrate` and `_init_data` fit well here.

*DEL_AREA* Temporary trash can. This will have its own gitignore to ignore_all in that subdirectory.

`APP`
Contains static and templates...


## Main Files
 *CONFIG.PY*, 
Primarily For DB setting;
Don't forget to input the local database via the environment vars;
Look to `config_vars`.

*APP/INIT* and *RUN.PY*
` __init__` for app and db creation; and
 these are auto-run when called by run.py

*MANAGER.PY*
manager.py sets up commands for you to use cmd directly.