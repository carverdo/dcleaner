// XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
// XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
var onoff = 0;
// DECLARATIONS AND RUN
// ============================================================
// point in time data captured from phone
var captures = {
    // start: Date(),
    // doSupported: false,
    // dmSupported: false
};
// var resHist = [];  // will collect our history of captures

// we set our declared variables in a function as we can later
// use that function as a reset
var vel = {}, pos = {}, cords = {};
var nIntervId; // interval stamps for our clock
var series = {  // default dots in graph
    name: 'Signature',
};
var rem = 3;  // countdown clock
// And run
motionVars();
getDeviceData();

// MAIN FUNCTIONS
// ============================================================
function getDeviceData() {
    // call motion
    if (window.DeviceMotionEvent) {
        window.addEventListener('devicemotion', MotionHandler, false);
    } else {
        document.getElementById("dmEvent").innerHTML = "Motion not supported."
    }
    // call orientation
    if (window.DeviceOrientationEvent) {
        window.addEventListener('deviceorientation', OrientationHandler, false);
    } else {
        document.getElementById("dmEvent2").innerHTML = "Orientation not supported."
    }
}

function MotionHandler(eventData) {
    /* Grab the acceleration from the results
    alpha is the compass direction
    beta is the front-to-back tilt in degrees, where front is positive
    gamma is the left-to-right tilt in degrees, where right is positive */
    /*
    var info, xyz = "[X, Y, Z, ra, rb, rg, a, b, g]"; d = Date();
    document.getElementById("dmEvent").innerHTML = "DeviceMotion";
    info = xyz.replace("X", round(eventData.acceleration.x));
    info = info.replace("Y", round(eventData.acceleration.y));
    info = info.replace("Z", round(eventData.acceleration.z));
    info = info.replace("ra", round(eventData.rotationRate.alpha));
    info = info.replace("rb", round(eventData.rotationRate.beta));
    info = info.replace("rg", round(eventData.rotationRate.gamma));
    document.getElementById("moCapture").innerHTML = info;
    info = eventData.interval;
    document.getElementById("moInterval").innerHTML = info;
    */
    // captures.dmSupported = true;
    // captures.interval = eventData.interval;
    captures.milli = new Date().getMilliseconds();
    captures.acc_x = round(eventData.acceleration.x);
    captures.acc_y = round(eventData.acceleration.y);
    captures.acc_z = round(eventData.acceleration.z);
    captures.ra = round(eventData.rotationRate.alpha);
    captures.rb = round(eventData.rotationRate.beta);
    captures.rg = round(eventData.rotationRate.gamma);
}

function OrientationHandler(eventData) {
    /* alpha is the compass direction
    beta is the front-to-back tilt in degrees, where front is positive
    gamma is the left-to-right tilt in degrees, where right is positive */
    /*
    var info, xyz = "[a, b, g]";
    document.getElementById("dmEvent2").innerHTML = "DeviceOrientation";
    info = xyz.replace("a", round(eventData.alpha));
    info = info.replace("b", round(eventData.beta));
    info = info.replace("g", round(eventData.gamma));
    document.getElementById("moCapture2").innerHTML = info;
    info = eventData.interval;
    document.getElementById("moInterval2").innerHTML = info;
    */
    // captures.doSupported = true;
    captures.dir_a = round(eventData.alpha);
    captures.dir_b = round(eventData.beta);
    captures.dir_g = round(eventData.gamma);
    captures.interval = round(eventData.interval);
}

// CONVENIENCE
// ============================================================
function round(val) {
    var amt = 10;
    return Math.round(val * amt) /  amt;
}

function motionVars() {
    // cumulative capture of velocity, pos;
    // co-ordinates is just pos restated for the graph;
    // set up like this allows us to reset these vars.
    vel = {
        x: [0],
        y: [0],
        z: [0]
    };
    pos = {
        x: [0],
        y: [0],
        z: [0]
    };
    cords = [{
        x: 0,
        y: 0,
        color: 'rgba(100, 100, 100, .5)'
    }];
}

function rescaleToColor(angle) {
    if (angle < 0) {
        angle += 360;
    }
    return angle * 255 / 360;
}

function countAndGo(fn_param) {
    // runs our timer first & then the main function with its parameters
    if (rem >= 0) {
        console.log(rem);
        document.getElementById('egg').innerHTML = rem;
        rem -= 1;
    } else {
        stopCollecting();
        rem = 3;
        document.getElementById('egg').innerHTML = "Capturing Data";
        // now for the main function
        task = fn_param[0];
        millis = fn_param[1];
        repeatit(task, millis, millis);
    }
}

function toggler() {
    onoff = 1 - onoff;
    document.getElementById('booler').innerHTML = onoff;
}


// RUNNING OUR SAMPLER
// ============================================================
function addCountDownLayer(task, millis) {
     repeatit(
        countAndGo, [task, millis], 1000
    );
}

function repeatit(task, param, millis) {
    nIntervId = setInterval(
        function() { task(param); }, millis);
}
function stopCollecting() {
    clearInterval(nIntervId);
    document.getElementById('egg').innerHTML = "Capture";
}

// VELOCITY CALCS
// ============================================================
function terminal_vel(millis) {
    var secs = millis / 1000;
    // run through our xyz axes
    for (var axis in vel) {
        var t_acc = 'acc_' + axis;
        // v = u + at
        var u = vel[axis].slice(-1)[0];
        var foo = Math.floor(Math.random() * 11) - 5;  // temp fudge
        var v = u + captures[t_acc] * secs + foo * onoff;  // temp fudge
        vel[axis].push(v);
        // s = (u + v) / 2 * t
        // but we want cumulative s
        pos[axis].push(
            pos[axis].slice(-1)[0] + (u + v ) * 0.5 * secs
        );
    }
    // turn our tilts into colours and gather
    var r = rescaleToColor(captures.dir_a) + Math.floor(Math.random() * 256) * onoff; //FUDGE
    var g = rescaleToColor(captures.dir_g) + Math.floor(Math.random() * 256) * onoff; //FFF
    var b = rescaleToColor(captures.dir_b) + Math.floor(Math.random() * 256) * onoff; //FFF
    var opacity = 0.5;
    // pop data xy co-ordinates
    cords.push({
        x: pos.x.slice(-1)[0],
        y: pos.y.slice(-1)[0],
        color: 'rgba(' + r + ',' + g + ',' + b + ',' + opacity + ')'
    });
    // populate page
    document.getElementById('pos').innerHTML = JSON.stringify(cords);
    document.getElementById('vel').innerHTML = JSON.stringify(vel);
    // populate our pre-defined chart with data
    series.data = cords;
    chartsettings.series = [series];
    $('#sigbox').highcharts(chartsettings);
}


// TEST FUNCTION
// ============================================================
/*
function flashText(cell_ref) {
    var oElem = document.getElementById(cell_ref);
    oElem.style.color = oElem.style.color == "red" ? "blue" : "red";
    terminal_vel(500);
    resHist.push(JSON.stringify(captures));
    oElem.innerHTML = resHist;
}
*/

