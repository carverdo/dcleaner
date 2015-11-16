/*
Capturing and modifying positional data for display on the phone.

Some refs -
http://stackoverflow.com/questions/18112729/calculate-compass-heading-from-deviceorientation-event-api
http://w3c.github.io/deviceorientation/spec-source-orientation.html#introduction
*/

// DECLARATIONS AND RUN
// some declared variables in a function as we can later reset
// ============================================================
var captures = {}; // point in time data captured from phone
var nIntervId; // interval stamps for our clock
var series = {  // default dots in graph
    name: 'Signature',
};
var rem = 2;  // countdown clock, 3 seconds

// AND RUN
// ============================================================
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

function OrientationHandler(eventData) {
    /*    Grab and modify rotation data
    alpha is the compass direction (rotation around z axis (out of face);
    varies 0 to 360;
    beta is the front-to-back tilt in degrees, where front is positive
    (so rotation around short x axis at base of phone);
    varies -180 to +180;
    gamma is rotation around the long y axis on LHS of phone;
    ie left-to-right tilt in degrees, where right is positive;
    varies -90 to +90 (so doesn't know if upside down);
    */
    captures.dir_a = round(eventData.alpha);
    captures.dir_b = round(eventData.beta);
    captures.dir_g = round(eventData.gamma);
    captures.northFace = compassHeading(
        captures.dir_a, captures.dir_b, captures.dir_g
    );
    document.getElementById('raws').innerHTML = [
        captures.dir_a, captures.dir_b, captures.dir_g
    ]; // temp fudge
    document.getElementById('compass').innerHTML = captures.northFace;
}

function MotionHandler(eventData) {
    /* Grab acceleration results */
    captures.acc_x = round(eventData.acceleration.x);
    captures.acc_y = round(eventData.acceleration.y);
    captures.acc_z = round(eventData.acceleration.z);
    document.getElementById('accs').innerHTML = [
        captures.acc_x, captures.acc_y, captures.acc_z
    ]; // temp fudge
}


// CONVERTING ALPHA
// ============================================================
function compassHeading(alpha, beta, gamma) {
    /* This function collapses the beta and gamma into alpha;
    To explain: where alpha is rotation about the z axis (coming
    out of the face of the phone, our new compassheading asks
    how northerly is the plane of the phone (as it extends
    out of the back) as this is how our user operates the phone.

    The exception to the rule is where the phone is totally flat;
    then the top the phone acts as north.
     */
    if (Math.abs(beta) < 5) {
        beta = 0;
    }
    if (Math.abs(gamma) < 5) {
        gamma = 0;
    }
    if (Math.abs(beta) != 0 || Math.abs(gamma) != 0) {
        // degrees to radians
        var alphaRad = alpha * (Math.PI / 180);
        var betaRad = beta * (Math.PI / 180);
        var gammaRad = gamma * (Math.PI / 180);
        // sines and cosines
        var sA = Math.sin(alphaRad);
        var sB = Math.sin(betaRad);
        var sG = Math.sin(gammaRad);
        var cA = Math.cos(alphaRad);
        var cB = Math.cos(betaRad);
        var cG = Math.cos(gammaRad);
        // Calculate A, B, G rotations
        var rA = - cA * sG - sA * sB * cG;
        var rB = - sA * sG + cA * sB * cG;
        var rG = - cB * cG;
        // Compass heading
        var compassHeading = Math.atan(rA / rB);
        // Convert compass heading to use whole unit circle
        if(rB < 0) {
            compassHeading += Math.PI;
        } else if(rA < 0) {
            compassHeading += 2 * Math.PI;
        }
        return Math.round(compassHeading * (180 / Math.PI)); // Compass Heading (in degrees)
    } else {
        revAlpha = 360 - alpha;
        return Math.round(revAlpha);
    }
}

// CONVENIENCES
// ============================================================
function round(val) {
    var amt = 100;
    return Math.round(val * amt) /  amt;
}

function motionVars() {
    // cumulative capture of velocity, disp;
    // co-ordinates is just disp restated for the graph;
    // set up like this allows us to reset these vars.
    vel = {
        x: [0],
        y: [0],
        z: [0]
    };
    disp = {
        x: [0],
        y: [0],
        z: [0]
    };
    cords = {
        x: [0],
        y: [0]
    };
    acc = {  // TEMP STORE
        x: [0],
        y: [0],
        z: [0]
    };
    bucketAcc = {  // TEMP STORE
        x: [0],
        y: [0],
        z: [0]
    };
    rot = {  // TEMP STORE
        theta: [0],
        beta: [0],
        gamma: [0]
    };
    cords2 = [{  // TEMP STORE
        x: 0,
        y: 0,
        // color: 'rgba(100, 100, 100, .5)'
    }];
}


// ==============================================
// NEW STUFF XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
// ==============================================
var ball   = document.querySelector('.ball');
var garden = document.querySelector('.garden');
var maxX = garden.clientWidth  - ball.clientWidth;
var maxY = garden.clientHeight - ball.clientHeight;

function handleOrientation(event) {
    var x = event.beta;  // In degree in the range [-180,180]
    var y = event.gamma; // In degree in the range [-90,90]

    document.getElementById('beta').innerHTML = "beta : " + x + "\n";
    document.getElementById('gamma').innerHTML = "gamma: " + y + "\n";

    // Because we don't want to have the device upside down
    // We constrain the x value to the range [-90,90]
    if (x >  90) { x =  90};
    if (x < -90) { x = -90};

    // To make computation easier we shift the range of
    // x and y to [0,180]
    x += 90;
    y += 90;

    // 10 is half the size of the ball
    // It center the positioning point to the center of the ball
    ball.style.top  = (maxX*x/180 - 10) + "px";
    ball.style.left = (maxY*y/180 - 10) + "px";
}

window.addEventListener('deviceorientation', handleOrientation);

