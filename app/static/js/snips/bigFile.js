/*
XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
*/
/* =========================
VARIABLES
========================= */
var di_changes = {}, di_suggs = {};
var choiceVar = [];
var page_ref = window.location.href.split('/');
// LoadChoices
var labers = $("#labers");
var newval = "";
// Logging
var usr_data = $("#usr_data").text();
var LOG_TITLE = "LOGGED", cName = "log_main", oName = "outlier";
// Painting our Datatables
var newScore = 0;
// Handling our columns and rows
var fo_co = $("#form_container");
// Thresholds, Regex
var l_limit = $("#l_limit"), u_limit = $("#u_limit"), bad_val = $("#bad_val");
var l_thresh, u_thresh, b_val;
var failed_chars = /[^A-Za-z0-9_\.]/;  // need the '.' so can't use \W+

/* =========================
RUN OUR FUNCTION
========================= */
$(document).ready(function() {
    // SIMPLE BIND EVENTS
    simpleBinds();
    // AJAX BINDS
    callingBinds();
});
/* =========================
SIMPLE BIND EVENTS
========================= */
function simpleBinds() {
    // displaying summary data
    var flip = $(".flip");
    flip.siblings().hide();
    flip.on('click', function() {
        $(this).siblings().slideToggle();
    });
    // colouring cells
    var cellRun = $(".cellRun");
    $.each(cellRun, function() {
        $(this).val() == 1 ? $(this).css("backgroundColor", "darkseagreen"):
            $(this).css("backgroundColor", "lightcoral");
        $(this).text($(this).val());
    });
    // re-colouring cells
    cellRun.on("click", function() {
        valToggler($(this));
        colorer($(this));
    });
    $(".rowRun").on("click", function() {
        var sibs = $(this).parents(".rowCont").find(".cellRun");
        $.each(sibs, function() {
            valToggler($(this));
            colorer($(this));
        });
    });
    // force columns
    $(".forceRun").on("click", function() {
        genUnfitData($(this));
    });
    // expanding headers
    $(".expander").children("div.headerStats").hide();
    $(".headerMouse").click(function() {
        // label-swapping
        var tmp = $(this).text();
        $(this).text(this.id);
        $(this).attr('id', tmp);
        // data outliers
        $(this).siblings(".headerStats").slideToggle();
    });
    $("form").on("submit", function(event) {
        event.preventDefault();
        $("#cur_val3").empty().append(cleanLog($(this)));
    });
}
/* =========================
EVENT-DRIVEN BIND EVENTS
========================= */
function callingBinds() {
    // STAMP DATA CHOICES TO FILE
    $("#stamper").click(function() {
        $(".cellRun").each(function() {
            choiceVar.push($(this).val());
        });
        $.post("../_stamp",
            JSON.stringify([page_ref.slice(-1)[0], choiceVar]),
            function(data, status) {
                $("#stamped").text("Data Saved.").fadeIn().fadeOut(2000);
            }
        );
    });
    // LOAD DATA CHOICES FROM FILE ONTO SCREEN
    $("#stampee").click(function() {
        $.post("../_load_stamp_list",
            page_ref.slice(-1)[0], function(data, status){
                labers.empty();
                var res = data.result;
                $.each(res, function (idx, val) {
                    addEle(val);
                    labers.append(newMeta);
                    labers.append($('<p>'));
                });
            }
        );
    });
    // LOAD THE STAMPED-DATA FILE ONTO CELLS
    $("div#labers").on("click", "a.stampLoaderClicks", function(){
        $.post("../_load_stampB", $(this).text(), function(data, status) {
            var res = data.result;
            $(".cellRun").each(function(idx, el) {
                newVal = res[idx];
                $(this).val(newVal);
                $(this).text((newVal==1 || newVal==0.1) ? 1: 0);
                colorer($(this));
            });
        });
    });
    // CRYSTALLISE YOUR LOGGING DATA
    $("#crystallise").click(function() {
        $.post("../_logcache",
            JSON.stringify([page_ref.slice(-1)[0], $(".log_row").text()]),
            function(data, status) {
                $("#stamped2").text("Data Saved.").fadeIn().fadeOut(2000);
            }
        );
    });
    // GET PREVAILING THRESHOLDS
    l_limit.on('blur keyup', function() { safeAdd($(this)) });
    u_limit.on('blur keyup', function() { safeAdd($(this)) });
    bad_val.on('blur keyup', function() { safeAdd($(this)) });
}
/* =========================
BUILD LOG MSGS
========================= */
function cleanLog(obj) {
    // separator
    var newLog = $("<div>");
    // headers
    var usr_data_RT = '||| ' + usr_data + ' | ' + $.now() + ' || ';
    var newRow = $("<h4>").text(usr_data_RT);
    newRow.attr("class", "log_row");
    // main body
    divers = obj.find("div");
    newLog.append(newRow);
    $.each(divers, function() {
        newRow = $("<p>");
        newRow.attr("class", "log_row");
        labs = $(this).children();
        boxes = $(this).children("input");
        tmp = "";
        tmp += labs.first().text();
        if (labs.last().text() != LOG_TITLE) {
            return true
        }
        tmp += " | " + labs.last().text();
        $.each(boxes, function() {
            tmp += " | " + $(this).attr("type");
            tmp += " | " + $(this).val();
        });
        tmp += " |\n ";
        newRow.text(tmp);
        newLog.append(newRow);
    })
    // footers
    newMeta = $("<p>");
    newMeta.text("||" + $("#meta").text());
    newMeta.attr("class", "log_row");
    newLog.append(newMeta);
    // and serialization data
    /* newSery = $("<p>");
    newSery.text(obj.serialize());
    newSery.attr("class", "log_row");
    newLog.append(newSery); */
    return newLog;
}

/* =========================
VALTOGGLER IS THE PRIMARY FUNCTION
CALLS GENUNFITDATA ANOTHER MAJOR FUNCTION
GUD IN TURN CALLS VALTOGGLER
========================= */
function valToggler(obj) {
    switch(parseFloat(obj.val())) {
        case 1:
            newScore = 0.9;
            break;
        case 0.9:
            newScore = 1;
            break;
        case 0:
            newScore = 0.1;
            break;
        case 0.1:
            newScore = 0;
            break;
    }
    obj.val(newScore);
    obj.text((newScore==1 || newScore==0.1) ? 1: 0);
    genUnfitData(obj);
}
function genUnfitData(obj) {
    tab = obj.parents("table");
    t_key = tab.find("th:first").text();
    // building di_changes
    if (obj[0].className == 'cellRun') {
        row = obj.parents(".rowCont");
        // rows = tab.find("tr.rowCont");
        r_key = row.find("button:first").text();
        cells = row.find(".cellRun");
        col_idx = cells.index(obj);
        rekeyDict(tab, t_key, r_key);
        val_extractor(tab, t_key, r_key, cells, col_idx);
        getThreshes();
    } else {
        row = obj.parents(".forceCont");
        r_key = row.find("button:first").text();
        cells = row.find(".forceRun");
        col_idx = cells.index(obj);
        rekeyDict(tab, t_key, r_key);
        val_extractorForce(tab, t_key, r_key, cells, col_idx);
        getThreshes();
    }
    $.post("../_bosh", JSON.stringify([page_ref.slice(-1)[0],
        di_changes, [l_thresh, u_thresh, b_val]]), function(data, status) {
        /* NOTE THE MAJOR DESIGN CHOICE HERE
        for simplicity we have chosen only [0];
        the effect of this is to take the results from the first column
        reading left to right */
        fo_co.empty();
        // dr holds error arrays for the column
        var dr = $(data.ffail_pack)[0];
        if (dr != undefined) {
            // add label & form for type-errors
            $.each(dr.ffails, function() {
                fo_co.append(form_ele_builder($(this)[1], $(this)[0], cName));
            });
        }
        // drO holds outliers
        // gapr is just labelling that splits up our drOs
        var drO = $(data.nonfail_pack)[0];
        var gapr = $(data.gapper)[0];
        if (gapr) {
            var glabs = ["MinMax (remaining)", "Uniques"];
            var prev_lab = [gapr.shift(), glabs.shift()];
        }
        if (drO != undefined) {
            // text for the outliers
            fo_co.append( $("<h5>").text("Values outside Limits") );
            fo_co.append(multi_builder('ALL OUTLIERS', oName));

            // again add for outliers (along with gap labels)
            $.each(drO.outliers, function(idx) {
                if (idx == prev_lab[0]) {
                    fo_co.append( $("<h5>").text(prev_lab[1]) );
                    prev_lab = [gapr.shift(), glabs.shift()];
                }
                fo_co.append(form_ele_builder($(this)[1], $(this)[0], oName));
            });
            // presentation in headers on excel table
            paintHeader(drO, t_key, col_idx);
        }
        // Add main text and buttons last
        var newTitle = $("<h5>"), newButton = $("<button>");
        newTitle.text("Type Errors and their current logging status");
        newButton.attr("class", "myButton");
        newButton.text("Submit all edits to the Logging Cache");
        if (dr != undefined) {
            fo_co.prepend(multi_builder(dr.ffails.length, cName));
        }
        fo_co.prepend(newButton);
        fo_co.prepend(newTitle);
    });
}
/* ==============================
THREE FNS CALLED UNDER _BOSH
============================== */
// BUILDS FORM ELEMENTS (for the error cases)
function form_ele_builder(datapack, labelpack, tag) {
    var newDiv = $("<div>"), newLabel = $("<label>"), newInput = $("<input>"),
        newQuery = $("<input>"), newButton = $("<button>");
    // the div holder
    newLabel.text(labelpack);
    // our elements
    /*newForm = $("<form>");
    newForm.attr("id", "form_container");
    input boxes */
    for (var key in datapack) {
        if (key == "css") {
            newInput.css("backgroundColor", datapack[key]);
            newInput.css("color", "white");
            continue;
        };
        newInput.attr(key, datapack[key]);
    };
    newInput.attr("required", false);
    // simple query boxes
    newQuery.attr('type', "search");
    newQuery.attr('name', "f_query");
    // building our buttons
    newButton.attr("class", "myButton " + tag);
    newButton.text("E");
    newButton.click(function(){
        var cur = $(this).parents("div").first();
        curbg = cur.css("backgroundColor");
        curbg == "rgba(0, 0, 0, 0)" ? cur.css("backgroundColor", "darkseagreen"):
        cur.css("backgroundColor", "rgba(0, 0, 0, 0)");
        $(this).text() == LOG_TITLE ? $(this).text("E"): $(this).text(LOG_TITLE);
    })
    // Append em all
    newDiv.append(newLabel);
    newDiv.append(newInput);
    newDiv.append(newQuery);
    newDiv.append(newButton);
    return newDiv;
}
// RELABELS HEADERS
function paintHeader(datapack, t_key, col_idx) {
    // just for presentation in main table (fills out data in header)
    if (datapack.tab_name == t_key && datapack.col_idx == col_idx) {
        // hr holds the data summary label for the col
        var hr = datapack.header, txt = "";
        $.each(hr, function(key, value){txt += key + " " + value + "<br>";});
        $(tab.find(".headerStats")[col_idx]).html(txt);
    }
}
// BUILDS MULTI BUTTON
function multi_builder(ct, classer){
    var multiButton = $("<button>");
    multiButton.attr("class", "myButton");
    multiButton.attr("id", "multi");
    multiButton.text('Set next ' + ct + ' buttons to ' + LOG_TITLE);
    multiButton.on("click", function(){
        $.each(fo_co.find('.' + classer), function () {
            $(this).text() == LOG_TITLE ? $(this).text("E"): $(this).text(LOG_TITLE);
        });
    });
    return multiButton;
}
/* ==============================
CALLED BY GENUNFITDATA
RETURNS ALL CELLS IN THAT COLUMN WHERE WE KNOW THE ACTUAL DATA
DIFFERS FROM THE ASSERTION OF TYPE(S)
============================== */
function val_extractor(tab, t_key, r_key, cells, col_idx) {
    // build good data types (for outlier analysis)
    tmp = suggestors_for_col(tab, col_idx);
    if (tmp[1] == 0 ) {good_labs = []} else {good_labs = tmp[0]};
    key_popper(di_changes, t_key, col_idx, good_labs);
    // build bad data-types
    bad_idx = fails_for_row(cells);
    key_popper(di_changes, t_key, r_key, bad_idx);
}
/* ==============================
VARIANT FOR THE CASE WHERE THERE IS NO PROBLEM
WE ARE FORCING THE RESULT
============================== */
function val_extractorForce(tab, t_key, r_key, cells, col_idx) {
    // build good data types (for outlier analysis)
    // this time we don't care that onoff = 0
    good_labs = suggestors_for_col(tab, col_idx)[0];
    key_popper(di_changes, t_key, col_idx, good_labs);
    // build bad data-types
    bad_labs = suggestors_for_col(tab, col_idx, 0)[0];
    $.each(bad_labs, function() {
        key_popper(di_changes, t_key, this, [col_idx]);
    });
    // get rid of ForceCol
    key_popper(di_changes, t_key, r_key, []);
}
/* ==============================
TWO FUNCTIONS CALLED BY VAL_EXTRACTOR
============================== */
// Finds titles of rows when cell.html = fval in the col_idx
function suggestors_for_col(tab, col_idx, fval) {
    if (fval === undefined) {fval = 1};
    var row_labs = [], onoff = 0;
    var rows = tab.find("tr.rowCont");
    rows.each(function() {
        cells = $(this).find(".cellRun");
        if (cells[col_idx].innerHTML == fval) {
            row_labs.push($(this).find("button.rowRun")[0].innerHTML);
        }
        // figures out if there are any errors in column
        switch(cells[col_idx].value) {
            case '1': break;
            case '0.9':
                onoff = 1;
                break;
        }
    });
    return [row_labs, onoff];
}
// Finds indexes of cols when cell.value = fval for those cells in row
function fails_for_row(cells, fval) {
    if (fval === undefined) {fval = 0.9};
    var c_idx = [], c_len = cells.length;
    for (var i = 0; i < c_len; i++) {
        if (cells[i].value == fval) {
            c_idx.push(i);
        };
    }
    return c_idx;
}
/* ==============================
THE DI_CHANGES DICTIONARY
DI_CHANGES holds good and bad data.

Good data is of the right type but is an outlier.
Bad data is the wrong data type.

Good data is stored by column, like this:
    di_changes[tkey][3] = ['text', 'number']
Bad data is stored across rows, like this:
    di_changes[tkey]['boolean] = [3]

onecol_Only is way of defaulting so that di_changes either holds
one or many columns of data
if onecol_only were set to false we would need to revisit the [0] defs for
dr and drO under _bosh
============================== */
function rekeyDict(tab, t_key, r_key, onecol_only) {
    if (onecol_only === undefined) {onecol_only = true}
    // if new tkey declare new dict according to onecol rule
    if (onecol_only) { di_changes[t_key] = {} } else {
        if (!(t_key in di_changes)) {
            di_changes[t_key] = {};
        }
    }
    // if new row_key declare a new list
    if (!(r_key in di_changes[t_key])) {
        di_changes[t_key][r_key] = [];
    }
}
function key_popper(di, key1, key2, obj) {
    if (obj.length > 0) {
         di[key1][key2] = obj;
    } else {
        delete di[key1][key2];
    }
}
/* ==============================
HELPER FUNCTIONS
============================== */
// SIMPLE BUILD OF ELEMENT
function addEle(txt) {
    var newMeta = $("<a>");
    newMeta.text(txt);
    newMeta.attr("class", "stampLoaderClicks");
    return newMeta;
}
// GATHER THRESHOLDS
function getThreshes() {
    // collect prevailing thresholds
    l_thresh = safeAdd(l_limit);
    u_thresh = safeAdd(u_limit);
    b_val = safeAdd(bad_val);
}
// TEXT ONLY FROM USER
function safeAdd(obj) {
    var v = obj.val();
    if (!failed_chars.test(v)) {
        return v;
    } else {
        return '';
    }
}
// COLORS
function colorer(obj) {
    curcol = (obj.text()==1) ? "forestgreen": "firebrick";
    obj.css("backgroundColor", curcol);
}