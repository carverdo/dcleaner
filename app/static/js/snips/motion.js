// Defines Function and Calls (producing return)
// ============================================================
init();

function init() {
    if ((window.DeviceMotionEvent) || ('listenForDeviceMovement' in window)) {
        window.addEventListener('devicemotion', deviceMotionHandler, false);
    } else {
        document.getElementById("dmEvent").innerHTML = "Not supported."
    }
}

function deviceMotionHandler(eventData) {
    document.getElementById("dmEvent").innerHTML = "DeviceMotion";

    var info, xyz = "[X, Y, Z]";
    // Grab the acceleration from the results
    var acceleration = eventData.acceleration;
    info = xyz.replace("X", round(acceleration.x));
    info = info.replace("Y", round(acceleration.y));
    info = info.replace("Z", round(acceleration.z));
    document.getElementById("moAccel").innerHTML = info;

    // Grab the acceleration including gravity from the results
    acceleration = eventData.accelerationIncludingGravity;
    info = xyz.replace("X", round(acceleration.x));
    info = info.replace("Y", round(acceleration.y));
    info = info.replace("Z", round(acceleration.z));
    document.getElementById("moAccelGrav").innerHTML = info;

    // Grab the rotation rate from the results
    var rotation = eventData.rotationRate;
    info = xyz.replace("X", round(rotation.alpha));
    info = info.replace("Y", round(rotation.beta));
    info = info.replace("Z", round(rotation.gamma));
    document.getElementById("moRotation").innerHTML = info;

    info = eventData.interval;
    document.getElementById("moInterval").innerHTML = info;
}

function round(val) {
    var amt = 10;
    return Math.round(val * amt) /  amt;
}