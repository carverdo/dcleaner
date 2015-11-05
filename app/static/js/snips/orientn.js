// Defines Function and Calls (producing return)
// ============================================================
init();

function init() {
    if (window.DeviceOrientationEvent) {
        document.getElementById("doEvent").innerHTML = "DeviceOrientation";
        // Listen for the deviceorientation event and handle the raw data
        window.addEventListener('deviceorientation', function(eventData) {
            // gamma is the left-to-right tilt in degrees, where right is positive
            var tiltLR = eventData.gamma + 0;

            // beta is the front-to-back tilt in degrees, where front is positive
            var tiltFB = eventData.beta + 0;

            // alpha is the compass direction the device is facing in degrees
            var dir = eventData.alpha + 0;

            // call our orientation event handler
            deviceOrientationHandler(tiltLR, tiltFB, dir);
            }, false);
    } else {
        document.getElementById("doEvent").innerHTML = "Not supported."
    }
}

function deviceOrientationHandler(tiltLR, tiltFB, dir) {
    document.getElementById("doTiltLR").innerHTML = Math.round(tiltLR);
    document.getElementById("doTiltFB").innerHTML = Math.round(tiltFB);
    document.getElementById("doDirection").innerHTML = Math.round(dir);

    // Apply the transform to the image
    var logo = document.getElementById("boxer");
    logo.style.webkitTransform = "rotate("+ tiltLR +"deg) rotate3d(1,0,0, "+ (tiltFB*-1)+"deg)";
    logo.style.MozTransform = "rotate("+ tiltLR +"deg)";
    logo.style.transform = "rotate("+ tiltLR +"deg) rotate3d(1,0,0, "+ (tiltFB*-1)+"deg)";
}

// Some other fun rotations to try...
//var rotation = "rotate3d(0,1,0, "+ (tiltLR*-1)+"deg) rotate3d(1,0,0, "+ (tiltFB*-1)+"deg)";
//var rotation = "rotate("+ tiltLR +"deg) rotate3d(0,1,0, "+ (tiltLR*-1)+"deg) rotate3d(1,0,0, "+ (tiltFB*-1)+"deg)";


// BUILDING AND RUNNER OUR SAMPLER
// ============================================================
var resHist = [];
var task = flashText;
var millis = 500;
var nIntervId;
var oElem = document.getElementById("echoLR");
repeatit(task, millis);

function repeatit(task, millis) {
    nIntervId = setInterval(task, millis);
}

function flashText() {
    oElem.style.color = oElem.style.color == "red" ? "blue" : "red";
    prevail = document.getElementById("doTiltLR").innerHTML;
    resHist.push(prevail);
    oElem.innerHTML = resHist;
}

function stopTextColor() {
    clearInterval(nIntervId);
}
