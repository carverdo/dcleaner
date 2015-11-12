/*
Capturing and modifying positional data for
display on the phone.

Some refs -
http://stackoverflow.com/questions/18112729/calculate-compass-heading-from-deviceorientation-event-api
http://w3c.github.io/deviceorientation/spec-source-orientation.html#introduction
*/
var onoff = 0;
var acc = {}; // TEMP STORE
var rot = {}; // TEMP STORE
// DECLARATIONS AND RUN
// we set some declared variables in a function as we can later
// use that function as a reset
// ============================================================
var captures = {}; // point in time data captured from phone
var vel = {}, pos = {}, cords = {}, cords2 = {};
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

function MotionHandler(eventData) {
    /* Grab acceleration results */
    captures.milli = new Date().getMilliseconds();
    captures.acc_x = round(eventData.acceleration.x);
    captures.acc_y = round(eventData.acceleration.y);
    captures.acc_z = round(eventData.acceleration.z);
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
    captures.interval = round(eventData.interval);
    captures.northFace = compassHeading(
        captures.dir_a, captures.dir_b, captures.dir_g
    );
    document.getElementById('accs').innerHTML = [
        Math.round(captures.acc_x), Math.round(captures.acc_y),
        Math.round(captures.acc_z)
    ]; // temp fudge


    document.getElementById('compass').innerHTML = captures.northFace;
    document.getElementById('raws').innerHTML = [
        captures.dir_a, captures.dir_b, captures.dir_g
    ]; // temp fudge
}

// RUNNING OUR SAMPLER
// ============================================================
function addCountDownLayer(task, millis) {
     repeatit(
        countAndGo, [task, millis], 1000  // reps 1sec on our countdown clock
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
        return revAlpha;
    }
}


// VELOCITY CALCS (this is the main onclick function)
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
        // v = u + at, but we need mean a;
        var u = vel[axis].slice(-1)[0];
        mean_a = (acc[axis].slice(-2)[0] + acc[axis].slice(-2)[1]) / 2;
        var v = u + mean_a * secs;
        vel[axis].push(v);
        // s = (u + v) / 2 * t, but we want cumulative s // pos[axis].slice(-1)[0] +
        ds = (u + v) * 0.5 * secs;
        pos[axis].push(
            ds
        );
    }
    // turn our tilts into colours and gather
    if (onoff == 1) {
        captures.dir_a = Math.floor(Math.random() * 256) * onoff; //FUDGE
        captures.dir_g = Math.floor(Math.random() * 256) * onoff; //FUDGE
        captures.dir_b = Math.floor(Math.random() * 256) * onoff; //FUDGE
        captures.northFace = Math.floor(Math.random() * 360); //FUDGE
    }
    rot['theta'].push(captures.northFace);
    rot['beta'].push(captures.dir_b);
    rot['gamma'].push(captures.dir_g);

    // pop data xy co-ordinates
    var eano = eastNorth(pos.x.slice(-1)[0], captures.northFace);
    cords2.push({
        x: eano[0] + cords2.slice(-1)[0]['x'],
        y: eano[1] + cords2.slice(-1)[0]['y'],
        color: rescaleToColor(captures.northFace)
    });

    cords.push({
        x: eano[0],  // pos.x.slice(-1)[0],  //
        y: eano[1], // pos.y.slice(-1)[0],  //
        color: rescaleToColor(captures.northFace)
    });

    // temp-pop //FUDGE
    document.getElementById('vex').innerHTML = round1(vel.x.slice(-1)[0]);
    document.getElementById('vey').innerHTML = round1(vel.y.slice(-1)[0]);
    document.getElementById('vez').innerHTML = round1(vel.z.slice(-1)[0]);



    // populate page
    document.getElementById('eano').innerHTML = JSON.stringify(cords2);
    document.getElementById('pos').innerHTML = JSON.stringify(cords);
    document.getElementById('vel').innerHTML = JSON.stringify(vel);
    document.getElementById('acc').innerHTML = JSON.stringify(acc);
    document.getElementById('rot').innerHTML = JSON.stringify(rot);
    // populate our pre-defined chart with data
    series.data = cords2; ///////////////////////////
    chartsettings.series = [series];
    $('#sigbox').highcharts(chartsettings);
}

// CONVENIENCES
// ============================================================
function round(val) {
    var amt = 10000;
    return Math.round(val * amt) /  amt;
}

function round1(val) {
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
    cords2 = [{  // TEMP STORE
        x: 0,
        y: 0,
        color: 'rgba(100, 100, 100, .5)'
    }];
}

function rescaleToColor(angle) {
    // opacity for northerly direction (of face);
    // red toward east; blue toward west;
    opacity = round(Math.abs(angle - 180) / 180);
    if (angle > 180) {
        color = 'rgba(0, 0, 255, ' + opacity + ')'
    } else {
        color = 'rgba(255, 0, 0, ' + opacity + ')'
    }
    if (angle == 0 || angle == 360) {
        color = 'rgba(0, 255, 0, ' + opacity + ')'
    }
    return color
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

function eastNorth(vec, theta) {
    rads = theta * Math.PI / 180;
    return [vec * Math.cos(rads), -vec * Math.sin(rads)];
}