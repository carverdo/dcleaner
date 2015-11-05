// Defines Function and Calls (producing return)
// ============================================================
var captures = {
    start: Date(),
    doSupported: false,
    dmSupported: false
};
init();

function init() {
    // call motion
    if (window.DeviceMotionEvent) {
        window.addEventListener('devicemotion', MotionHandler, false);
    } else {
        document.getElementById("dmEvent").innerHTML = "Not supported."
    }
    // call orientation
    if (window.DeviceOrientationEvent) {
        window.addEventListener('deviceorientation', OrientationHandler, false);
    } else {
        document.getElementById("dmEvent2").innerHTML = "Not supported."
    }
}

function MotionHandler(eventData) {
    var info, xyz = "[X, Y, Z, ra, rb, rg, a, b, g]"; d = Date();
    document.getElementById("dmEvent").innerHTML = "DeviceMotion";
    /* Grab the acceleration from the results
    alpha is the compass direction
    beta is the front-to-back tilt in degrees, where front is positive
    gamma is the left-to-right tilt in degrees, where right is positive */
    info = xyz.replace("X", round(eventData.acceleration.x));
    info = info.replace("Y", round(eventData.acceleration.y));
    info = info.replace("Z", round(eventData.acceleration.z));
    info = info.replace("ra", round(eventData.rotationRate.alpha));
    info = info.replace("rb", round(eventData.rotationRate.beta));
    info = info.replace("rg", round(eventData.rotationRate.gamma));
    document.getElementById("moCapture").innerHTML = info;
    info = eventData.interval;
    document.getElementById("moInterval").innerHTML = info;

    captures.dmSupported = true;
    captures.milli = new Date().getMilliseconds();
    captures.x = round(eventData.acceleration.x);
    captures.y = round(eventData.acceleration.y);
    captures.z = round(eventData.acceleration.z);
    captures.ra = round(eventData.rotationRate.alpha);
    captures.rb = round(eventData.rotationRate.beta);
    captures.rg = round(eventData.rotationRate.gamma);
    captures.interval = eventData.interval;

    console.log(captures);
    console.log(12);
}


function OrientationHandler(eventData) {
    var info, xyz = "[a, b, g]";
    document.getElementById("dmEvent2").innerHTML = "DeviceOrientation";
    /* alpha is the compass direction
    beta is the front-to-back tilt in degrees, where front is positive
    gamma is the left-to-right tilt in degrees, where right is positive */
    info = xyz.replace("a", round(eventData.alpha));
    info = info.replace("b", round(eventData.beta));
    info = info.replace("g", round(eventData.gamma));
    document.getElementById("moInterval2").innerHTML = info;
    info = eventData.interval;
    document.getElementById("moCapture2").innerHTML = info;

    captures.doSupported = true;
    captures.a = round(eventData.alpha);
    captures.b = round(eventData.beta);
    captures.g = round(eventData.gamma);

    console.log(captures);
    console.log(13);
}


function round(val) {
    var amt = 10;
    return Math.round(val * amt) /  amt;
}


// BUILDING AND RUNNER OUR SAMPLER
// ============================================================
var resHist = [];
var task = flashText, millis = 500, nIntervId;
var oElem = document.getElementById("echoMotion");

resHist.push(captures.start);

function repeatit(task, millis) {
    nIntervId = setInterval(task, millis);
}

function flashText() {
    oElem.style.color = oElem.style.color == "red" ? "blue" : "red";
    var prevail = [
        captures.milli,
        captures.b,
        captures.g
    ];
    resHist.push(prevail);
    oElem.innerHTML = resHist;
}

function stopCollecting() {
    clearInterval(nIntervId);
}
