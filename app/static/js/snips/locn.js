// Defines Function and Calls (producing return)
// ============================================================
var crd;
getLocation();

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(success);
    } else {
    popEle("lalo", "Geolcation switched off or not supported.");
    }
}

function success(pos) {
    crd = pos.coords;
    res = {'lat': crd.latitude, 'long': crd.longitude};

    // sends it back for database handling
    $.getJSON('./_clientdata', res, function(data) {
        $("#result").text(data.result);
    });
    // not necessarily echoed in template
    popEle("lalo", JSON.stringify(res));

}

function popEle(name, val) {
    x = document.getElementById(name);
    x.innerHTML = val;
}

