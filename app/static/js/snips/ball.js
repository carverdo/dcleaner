/*
Capturing and modifying positional data for display on the phone.

Some refs -
https://developer.mozilla.org/en-US/docs/Web/API/Detecting_device_orientation
http://stackoverflow.com/questions/18112729/calculate-compass-heading-from-deviceorientation-event-api
http://w3c.github.io/deviceorientation/spec-source-orientation.html#introduction
*/

// DECLARATIONS AND INSTANTIATING DEVICE
// some declared variables in a function as we can later reset
// ============================================================
var onoff = 0;
var stamp, elapse, elapseMin = 50; // milliseconds
var tiltStamp = 0, remTime, elapseMax = 6000; // milliseconds
var tiltAngle = 7; // degrees
var accThresh = 5; // metres per sec squared
var tallyM = 3, tallyS = 5, tallyE = 11;  // counters: middle (halfway to start), start, end
var ball = document.querySelector('.ball');
var garden = document.querySelector('.garden');
var maxX = garden.clientWidth  - ball.clientWidth;
var maxY = garden.clientHeight - ball.clientHeight;

motionVars();
// setShaker();
getDeviceData();

// MAIN DEVICE FUNCTIONS
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
    dir_a = round(eventData.alpha);
    dir_b = round(eventData.beta);
    dir_g = round(eventData.gamma);
    northFace = compassHeading(
        dir_a, dir_b, dir_g
    );
    document.getElementById('raws').innerHTML = [
        dir_a, dir_b, dir_g
    ]; // temp fudge
    document.getElementById('compass').innerHTML = northFace;
}

function MotionHandler(eventData) {
    /* Grab acceleration results */
    interval = eventData.interval;
    acc_x = round(eventData.acceleration.x);
    acc_y = round(eventData.acceleration.y);
    acc_z = round(eventData.acceleration.z);
    document.getElementById('accs').innerHTML = [
        acc_x, acc_y, acc_z
    ]; // temp fudge
    document.getElementById('ival').innerHTML = [
        interval
    ]; // temp fudge
}


// CONVERTING ALPHA
// ============================================================
function compassHeading(alpha, beta, gamma) {
    /* This function collapses the beta and gamma into alpha;
    To explain: where alpha is rotation about the z axis (coming
    out of the face of the phone, our new compassHeading asks
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
    prevTilt = 0;
    tallyTilt = 0;
    stamp = Date.now();
    tiltStamp = 0;
    playedOnce = false;
    prettyButtons('off', elapseMax);

    acc = {  // TEMP STORE
        x: [0],
        y: [0],
        z: [0]
    };
    rot = {  // TEMP STORE
        theta: [0],
        beta: [0],
        gamma: [0]
    };
    /*
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
    bucketAcc = {  // TEMP STORE
        x: [0],
        y: [0],
        z: [0]
    };
    cords2 = [{  // TEMP STORE
        x: 0,
        y: 0,
        // color: 'rgba(100, 100, 100, .5)'
    }];
    */
}

function toggler() {
    onoff = 1 - onoff;
    if (onoff == 1) {
        $('#booler').text('RecorderReady');
        $('#booler').css('color', 'White');
        $('#remTime').attr('class', 'label label-danger');
        $('#remTime').text('ShakeAndSign');
        $('#beep6').get(0).play();
    } else {
        $('#booler').text('RecorderOff');
        $('#booler').css('color', 'Orange');
        $('#remTime').text('');
    }
}

function prettyButtons(power, rem) {
    rem = round(rem / 1000);
    if (power == 'on') {
        $('#remTime').attr('class', 'label label-success');
        $('#remTime').text('Remaining: ' + rem + ' secs');
        // $('#captButton').show(1000).hide(1000);
        $("#paBody").css("background-color", "#04d70b"); // green
        $("#paBody").css('background-image', 'none');
    } else {
        /*
        $('#remTime').attr('class', 'label label-default');
        $('#remTime').text('ShakeToSign');
        */
        // $('#captButton').hide();
        $("#paBody").css("background-color", "#ffffff"); // white
        $("#paBody").css('background-image', 'url(' + './static/image/shakephone3.png' +')');
    }
}

// ==============================================
// MAIN OPERATIVE FUNCTIONS
// ==============================================
function runShaker(tilt, maxAcc) {
    // When user does a -+ tilt at speed, we increase our tally;
    // prevTilt holds the prevailing (and then previous result);
    // Tally has a start and a stop level;
    if (tilt < - tiltAngle && maxAcc > accThresh) {
        if (prevTilt >= 0) {
            tallyTilt += 1;
        }
        prevTilt = -1;
    } else if (tilt > tiltAngle && maxAcc > accThresh) {
        if (prevTilt < 0) {
            tallyTilt += 1;
        }
        prevTilt = 1;
    }
    $("#pOnce").text(tallyTilt);
    remTime = elapseMax - ((tiltStamp == 0) ? 0 : Date.now() - tiltStamp);
    // document.getElementById('remTime').innerHTML = 'Stopwatch: ' + round(remTime / 1000) + ' secs';
    // Pass data and reset our vars
    if (tallyTilt >= tallyE || remTime <= 0) {
        passMotionData();
        motionVars();
    }
}

function passMotionData() {
    // sends it back for database handling
    var strData = {
        'strAcx': JSON.stringify(acc['x']), //.slice(0, 5)),
        'strAcy': JSON.stringify(acc['y']),
        'strTheta': JSON.stringify(rot['theta']),
        'strBeta': JSON.stringify(rot['beta']),
        'strGamma': JSON.stringify(rot['gamma'])
    }
    $.getJSON('./_balldata', strData, function(data) {
        $("#result").text("Signature received.").fadeOut(8000); // .text(data.ballData);
    });
};

function handleOrientation(event) {
    // var x = event.beta;  // In degree in the range [-180,180]
    // var y = event.gamma; // In degree in the range [-90,90]
    // document.getElementById('beta').innerHTML = "x : " + x + "\n";
    // document.getElementById('gamma').innerHTML = "y : " + y + "\n";
    /*
    // Because we don't want to have the device upside down
    // We constrain the x value to the range [-90,90]
    if (x >  90) { x =  90};
    if (x < -90) { x = -90};

    // To make computation easier we shift the range of
    // x and y to [0,180]
    x += 90;
    y += 90;
    */
    // 10 is half the size of the ball
    // It center the positioning point to the center of the ball
    ball.style.left  = (maxX * (acc_x / 10 + 0.5) ) + "px";
    ball.style.top = (maxY * (-acc_y / 10 + 0.5) ) + "px";

    if (onoff == 1) {
        // record snapshot if we get signal
        runShaker(dir_g, Math.max(Math.abs(acc_x), Math.abs(acc_y)));
        // otherwise keep capturing data
        elapse = Date.now() - stamp;
        if (tallyTilt >= tallyS && elapse >= elapseMin) {
            prettyButtons('on', remTime);
            acc['x'].push(acc_x);
            acc['y'].push(acc_y);
            rot['theta'].push(northFace);
            rot['beta'].push(dir_b);
            rot['gamma'].push(dir_g);
            // start tilt clock
            if (tiltStamp == 0 ) {
                tiltStamp = Date.now();
            }
            stamp = Date.now();
            /* , display
            document.getElementById('acx').innerHTML = acc['x'].length;
            document.getElementById('acy').innerHTML = acc['y'];
            document.getElementById('theta').innerHTML = rot['theta'];
            document.getElementById('beta').innerHTML = rot['beta'];
            document.getElementById('gamma').innerHTML = rot['gamma'];
            */
        } else if (tallyTilt >= tallyM && ! Boolean(playedOnce) ) {
            $('#remTime').attr('class', 'label label-warning');
            $("#paBody").css("background-color", "#fcaa1d");  // amber
            $("#paBody").css('background-image', 'none');
            $('#beep6').get(0).play();
            playedOnce = true;
        }
    }
}

// AND RUN
// ============================================================
window.addEventListener('deviceorientation', handleOrientation);

$(document).on('click', '.toggle-button', function() {
    $(this).toggleClass('toggle-button-selected');
    toggler();
});