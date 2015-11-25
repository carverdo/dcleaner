/*
We want to set click events dynamically
and here in jscript world otherwise you
can end up with page load (repeat event) errors.

Doesn't actually delete the row.
Passes back the ro.id to python for it to delete the entry.
*/
setBinders();

function setBinders() {
    // collating clickable events and applies function;
    var withIds = $('button[id]').each(function() {
        if ($(this).attr('id')) {
            $(this).bind("click", getRowID);
        }
    });
};


function getRowID() {
    // takes the element, ids it,
    // sends it back for database handling;
    // url, data, function on success
    res = {'strMemID': this.id};
    $.getJSON('./_balldata', res, function(data) {
        $("#deletedRow").text("Deleted row: " + data.ballData);
    });
};
