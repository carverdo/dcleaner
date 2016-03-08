/*
XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
*/
/* =========================
VARIABLES
========================= */
var di_changes = {}, di_suggs = {};
var choiceVar = [];
/* LoadChoices */
var labers = $("#labers");
var res = [], newval="";
/* Logging */
var usr_data = $("#usr_data").text(), usr_data_RT = "", tmp = "";
/* Painting our Datatables */
var newScore = 0;
/* Handling our columns and rows */
var datapack, row_labs = [], onoff = 0, c_idx = [];
/* =========================
RUN OUR FUNCTION
========================= */
$(document).ready(function() {
    /* SIMPLE BIND EVENTS */
    simpleBinds();
    /* AJAX BINDS */
    callingBinds();
});
/* =========================
SIMPLE BIND EVENTS
========================= */
function simpleBinds() {
    $(".flip").siblings().hide();
    $(".flip").on("mouseover mouseout", function() {
        $(this).siblings().slideToggle();
    })
    $.each($(".cellRun"), function() {
        $(this).val() == 1 ? $(this).css("backgroundColor", "darkseagreen"):
            $(this).css("backgroundColor", "lightcoral");
        $(this).text($(this).val());
    })
    $(".cellRun").on("click", function() {
        valToggler($(this));
        colorer($(this));
    })
    $(".rowRun").on("click", function() {
        row = $(this).parents(".rowCont");
        sibs = row.find(".cellRun");
        $.each(sibs, function() {
            valToggler($(this));
            colorer($(this));
        })
    })
    $(".expander").children("div.headerStats").hide();
    $(".expander").click(function() {
        $(this).children(".headerStats").slideToggle();
    })
    $("form").on("submit", function(event) {
        event.preventDefault();
        $("#cur_val3").empty();
        $("#cur_val3").append(cleanLog($(this)));
    });
}
/* =========================
CALLING BIND EVENTS
========================= */
function callingBinds() {
    /* STAMP DATA CHOICES TO FILE */
    $("#stamper").click(function() {
        $(".cellRun").each(function() {
            choiceVar.push($(this).val());
        });
        $.post("./_stamp", JSON.stringify(choiceVar), function(data, status) {
            $("#stamped").text("Data Saved.").fadeIn().fadeOut(2000);
        });
    });
    /* LOAD DATA CHOICES FROM FILE ONTO SCREEN */
    $("#stampee").click(function() {
        $.post("./_load_stamp_list", function(data, status){
            labers.empty();
            res = data["result"];
            $.each(res, function (idx, val) {
                addEle(val);
                labers.append(newMeta);
            });
        });
    });
    /* LOAD THE STAMPED-DATA FILE */
    /* VERSION 1 USING REAL FILE FORM NO LONGER USED
    $("#stampLoader").change(function() {
        $.post("./_load_stamp", $(this).val(), function(data, status) {
            res = $.parseJSON(data["result"]);
            $(".cellRun").each(function(idx, el) {
                newVal = res[idx];
                $(this).val(newVal);
                $(this).text((newVal==1 || newVal==0.1) ? 1: 0);
                colorer($(this));
            });
            genUnfitData($(".cellRun:first"));
        });
    });
    */
    /* VERSION 2 */
    $("div#labers").on("click", "p.stampLoaderClicks", function(){
        $.post("./_load_stampB", $(this).text(), function(data, status) {
            res = data["result"];
            $(".cellRun").each(function(idx, el) {
                newVal = res[idx];
                $(this).val(newVal);
                $(this).text((newVal==1 || newVal==0.1) ? 1: 0);
                colorer($(this));
            });
        });
    });
    /* CRYSTALLISE YOUR LOGGING DATA */
    $("#crystallise").click(function() {
        $.post("./_logcache", JSON.stringify($(".log_row").text()), function(data, status) {
            $("#stamped2").text("Data Saved.").fadeIn().fadeOut(2000);
        });
    });
}
/* =========================
CONVENIENCE FUNCTIONS
========================= */
/* Tidy Up Log Msg */
function cleanLog(obj) {
    /* separator */
    newLog = $("<div>");
    /* headers */
    usr_data_RT = usr_data + ' | ' + $.now();
    newRow = $("<h4>").text(usr_data_RT);
    newRow.attr("class", "log_row");
    /* main body */
    divers = obj.find("div");
    newLog.append(newRow);
    /* newLog.append(burr); */
    $.each(divers, function() {
        newRow = $("<p>");
        newRow.attr("class", "log_row");
        labs = $(this).children();
        boxes = $(this).children("input");
        tmp = "";
        tmp += labs.first().text();
        tmp += " | " + labs.last().text();
        $.each(boxes, function() {
            tmp += " | " + $(this).attr("type");
            tmp += " | " + $(this).val();
        });
        tmp += " | ";
        newRow.text(tmp);
        newLog.append(newRow);
    })
    /* footers */
    newMeta = $("<p>");
    newMeta.text("\n" + $("#meta").text());
    newMeta.attr("class", "log_row");
    newLog.append(newMeta);
    /* and serialization data */
    newSery = $("<p>");
    newSery.text("\n" + obj.serialize());
    newSery.attr("class", "log_row");
    newLog.append(newSery);
    return newLog
}
/* OPERATIVE FUNCTIONS ON CLICK */
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
function colorer(obj) {
    curcol = (obj.text()==1) ? "forestgreen": "firebrick";
    obj.css("backgroundColor", curcol);
}
function genUnfitData(obj) {
    tab = obj.parents("table");
    row = obj.parents(".rowCont");
    rows = tab.find("tr.rowCont");
    t_key = tab.find("th:first").text();
    r_key = row.find("button:first").text();
    cells = row.find(".cellRun");
    col_idx = cells.index(obj);
    val_extractor(tab, t_key, r_key, cells, col_idx);
    $.post("./_bosh", JSON.stringify(di_changes), function(data, status) {
        /* Container Styling */
        $("#form_container").empty();
        newTitle = $("<p>");
        newTitle.text("Errors and their current logging status");
        $("#form_container").append(newTitle);
        newButton = $("<button>");
        newButton.attr("class", "myButton");
        newButton.text("Submit all edits to the Logging Cache");
        $("#form_container").append(newButton);
        /* The rows of data; each a form */
        /* Data summaries for each column that has changed */
        ff_datapacks = $(data["ffail_pack"]);
        ff_datapacks.each(function() {
            datapack = $(this)[0];
            /* dr holds error arrays for the column */
            dr = datapack["ffails"];
            $.each(dr, function() {
                labelpack = $(this)[0];
                d_pack = $(this)[1];
                $("#form_container").append(form_ele_builder(
                    d_pack, labelpack));
            });
        })
        /* Data summaries for the outliers */
        newTitle = $("<p>");
        newTitle.text("Outliers (Min, Max, Uniques)");
        $("#form_container").append(newTitle);
        nf_datapacks = $(data["nonfail_pack"]);
        nf_datapacks.each(function() {
            datapack = $(this)[0];
            /* is this datapack the live/clicked case? */
            if (datapack["tab_name"] == t_key &&
                    datapack["col_idx"] == col_idx) {
                /* hr holds the data summary label for the col */
                hr = datapack["header"];
                txt = "";
                $.each(hr, function(key, value){
                    txt += key + " " + value + "<br>";
                })
                $(tab.find(".headerStats")[col_idx]).html(txt);
            }
            /* dr holds the outlier column */
            dr = datapack["outliers"];
            $.each(dr, function() {
                labelpack = $(this)[0];
                d_pack = $(this)[1];
                $("#form_container").append(form_ele_builder(
                    d_pack, labelpack));
            });
        })
    });
}
/* BUILDS FORM ELEMENTS (for the error cases) */
function form_ele_builder(datapack, labelpack) {
    /* the div holder */
    newDiv = $("<div>");
    newLabel = $("<label>");
    newLabel.text(labelpack);
    /* the form container */
    /* newForm = $("<form>"); */
    /* newForm.attr("id", "form_container"); */
    /* input boxes */
    newInput = $("<input>");
    for (var key in datapack) {
        if (key == "css") {
            newInput.css("backgroundColor", datapack[key]);
            newInput.css("color", "white");
            continue;
        };
        newInput.attr(key, datapack[key]);
    };
    newInput.attr("required", false);
    /* simple query boxes */
    newQuery = $("<input>");
    newQuery.attr('type', "search");
    newQuery.attr('name', "f_query");
    /* building our buttons */
    newButton = $("<button>");
    newButton.attr("class", "myButton");
    newButton.text("E");
    newButton.click(function(){
        cur = $(this).parents("div").first();
        curbg = cur.css("backgroundColor");
        curbg == "rgba(0, 0, 0, 0)" ? cur.css("backgroundColor", "darkseagreen"):
        cur.css("backgroundColor", "rgba(0, 0, 0, 0)");
        $(this).text() == "LOGGED" ? $(this).text("E"): $(this).text("LOGGED");
    })
    /* Append em all */
    newDiv.append(newLabel);
    newDiv.append(newInput);
    newDiv.append(newQuery);
    newDiv.append(newButton);
    return newDiv;
}

/* RETURNS ALL CELLS IN THAT COLUMN WHERE WE KNOW THE ACTUAL DATA
DIFFERS FROM THE ASSERTION OF TYPE(S) */
function val_extractor(tab, t_key, r_key, cells, col_idx) {
    if (!(t_key in di_changes)) {
        di_changes[t_key] = {};
    }
    if (!(r_key in di_changes[t_key])) {
        di_changes[t_key][r_key] = [];
    }
    row_labs = suggestors_for_col(tab, col_idx);
    key_popper(di_changes, t_key, col_idx, row_labs);
    col_labs = fails_for_row(cells);
    key_popper(di_changes, t_key, r_key, col_labs);
}

/* THREE FUNCTIONS CALLED BY VAL_EXTRACTOR */
function suggestors_for_col(tab, cref) {
    rows = tab.find("tr.rowCont");
    row_labs = [];
    onoff = 0;
    rows.each(function() {
        cells = $(this).find(".cellRun");
        if (cells[cref].innerHTML == 1) {
            row_labs.push($(this).find("button.rowRun")[0].innerHTML);
        }
        switch(cells[cref].value) {
            case '1': break;
            case '0.9':
                onoff = 1;
                break;
        }
    })
    if (onoff == 0) {row_labs = []};
    return row_labs
}
function fails_for_row(cells) {
    c_idx = [];
    c_len = cells.length;
    for (i = 0; i < c_len; i++) {
        if (cells[i].value == 0.9) {
            c_idx.push(i);
        };
    }
    return c_idx;
}
function key_popper(di, key1, key2, obj) {
    if (obj.length > 0) {
         di[key1][key2] = obj;
    } else {
        delete di[key1][key2];
    }
}
/* SIMPLE BUILD OF ELEMENT */
function addEle(txt) {
    newMeta = $("<p>");
    newMeta.text(txt);
    newMeta.attr("class", "stampLoaderClicks");
    return newMeta;
}
