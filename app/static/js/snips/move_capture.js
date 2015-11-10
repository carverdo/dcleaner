// XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
// XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
var onoff = 0;
var acc = {}; // TEMP STORE
var rot = {}; // TEMP STORE
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
var rem = 2;  // countdown clock, 3 seconds
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
    // captures.ra = round(eventData.rotationRate.alpha);
    // captures.rb = round(eventData.rotationRate.beta);
    // captures.rg = round(eventData.rotationRate.gamma);
}

function OrientationHandler(eventData) {
    /*
    alpha is the compass direction (rotation around z axis);
    varies 0 to 360;
    beta is rotation around the long y axis on LHS of phone;
    varies -90 to +90 (so doesn't know if upside down);
    think of as capturing the off-horizontal;
    gamma is rotation around short x axis at base of phone;
    varies -180 to +180;
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
    var true_a = Math.round(eventData.alpha);
    var true_b = Math.round(eventData.beta);
    var true_g = Math.round(eventData.gamma);
    document.getElementById('raws').innerHTML = [
        true_a, true_b, true_g
    ]; // temp fudge
    captures.dir_a = Math.round(Math.abs(round(eventData.alpha) - 180));
    captures.dir_b = Math.round(Math.abs(round(eventData.beta)));
    captures.dir_g = Math.round(Math.abs(round(eventData.gamma)) * 2);
    captures.interval = round(eventData.interval);
    document.getElementById('north').innerHTML = [
        captures.dir_a, captures.dir_b, captures.dir_g
    ]; // temp fudge
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
        var foo = Math.floor(Math.random() * 11) - 5.5;  // temp fudge
        if (onoff != 0) {
            captures[t_acc] = foo;  // temp fudge
        };
        acc[axis].push(captures[t_acc]);  // temp store
        // v = u + at
        // we need mean a;
        var u = vel[axis].slice(-1)[0];
        mean_a = ( acc[axis].slice(-2)[0] + acc[axis].slice(-2)[1] ) / 2;
        var v = u + mean_a * secs;
        vel[axis].push(v);
        // s = (u + v) / 2 * t
        // but we want cumulative s
        pos[axis].push(
            pos[axis].slice(-1)[0] + (u + v) * 0.5 * secs
        );
    }
    // turn our tilts into colours and gather
    var r = captures.dir_a * (1 - onoff) + Math.floor(Math.random() * 256) * onoff; //FUDGE
    var g = captures.dir_g * (1 - onoff) + Math.floor(Math.random() * 256) * onoff; //FFF
    var b = captures.dir_b * (1 - onoff) + Math.floor(Math.random() * 256) * onoff; //FFF
    rot['r'].push(r);
    rot['g'].push(g);
    rot['b'].push(b);
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
    document.getElementById('acc').innerHTML = JSON.stringify(acc);
    document.getElementById('rot').innerHTML = JSON.stringify(rot);
    // populate our pre-defined chart with data
    series.data = cords;
    chartsettings.series = [series];
    $('#sigbox').highcharts(chartsettings);
}

// CONVENIENCES
// ============================================================
function round(val) {
    var amt = 1000;
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
    acc = {  // TEMP STORE
        x: [0],
        y: [0],
        z: [0]
    };
    rot = {  // TEMP STORE
        r: [0],
        b: [0],
        g: [0]
    };

}

function rescaleToColor(angle) {
    // we only measure along one direction;
    if (angle < 0) {  // all positive;
        angle += 360;
    }
    angle -= 180;  // reverse polarity for coloring;
    if (angle <= 0) {  // ignore plus/minus;
        angle *= -1;
    }
    return Math.floor(angle * 255 / 180);
}

function countAndGo(fn_param) {
    // runs our timer first & then the main function with its parameters
    if (rem >= 0) {
        document.getElementById('egg').innerHTML = rem;
        rem -= 1;
    } else {
        stopCollecting();
        rem = 2;
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

