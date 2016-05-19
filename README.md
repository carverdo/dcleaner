# Getting Started
Project allows for the authenTicated user to upload to the s3 directory a file
that needs to be cleaned.
There may be numerous files in the s3 directory, so dataSets allows user to
provide the name of the dataset to focus on.
This then loads up the (excel) data for display.

## DataCleaning
On loading, all data is type-tested and for each column data-types are
marked as present/absent (1/0).
User looks for columns that seem to be populated with the wrong data-type; as a
general rule-of-thumb each column should only have one data-type.
User asserts the correct type-constraint on the column (by setting 1s to 0s and
vice versa) generating error columns in the logging section beneath which
user can then comment upon.

###RecordChanges / LoadPreviousChanges
On each page refresh the data read is also refreshed (and thus any user-entered
type assertions lost); to prevent this user can take a snapshot of their edits
at any point and reload onto the page.

###Building Log
Type assertions automatically generate type errors followed by value outliers
beneath.

Each of those entries can be examined individually, with an individual logging
decision executed by the button to the right.

For each log entry suggested values can be inserted as well as comments added.

###Logging Cache / Record
Those logs sit in a log cache ready for final review prior to submitting
for record.

Any unsatisfactory entry can be edited or removed simply by going back to
the row it was submitted from and amending accordingly.

The records of log build up sequentially in time order for each project so that
user can simply go back to the s3 directory and download the last logfile
associated with their project.

Copy that textfile into excel for easy viewing.

###logsView
Alternatively, logsView allows you to do same on the screen.