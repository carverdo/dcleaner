/*
Just some trash to auto-run
*/

// DECLARATIONS AND INSTANTIATING DEVICE
// some declared variables in a function as we can later reset
// ============================================================
var onoff = 0;
var stamp;
var tiltStamp = 0, remTime, elapseMax = 5000; // milliseconds
tallyE = 4;  // counters: middle (halfway to start), start, end
var ball = document.querySelector('.ball');

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
}

function toggler() {
    console.log(onoff);
    onoff = 1 - onoff;
    console.log(onoff);
    if (onoff == 1) {
        $('#booler').text('RecorderReady');
        $('#booler').css('color', 'White');
        $('#remTime').attr('class', 'label label-danger');
        $('#remTime').text('x3 shakes and sign');
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
        $("#paBody").css("background-color", "#04d70b"); // green
        $("#paBody").css('background-image', 'none');
    } else {
        if (onoff == 1) {
            $('#remTime').attr('class', 'label label-danger');
            $('#remTime').text('x3 shakes and sign');
        }
        $("#paBody").css("background-color", "#ffffff"); // white
        $("#paBody").css('background-image', 'url(' + './static/image/shakephone3.png' +')');
    }
}

function setTagVal() {
    // Input box shows current value and
    // allows user to set a new one
    var input = document.getElementById("tagVal");
    if (localStorage && 'tagVal' in localStorage) {
        input.value = localStorage.tagVal;
    }
    document.getElementById("setTag").onclick = function () {
        localStorage && (localStorage.tagVal = input.value);
    };
}

// ==============================================
// MAIN OPERATIVE FUNCTIONS
// ==============================================
function runShaker(tilt, maxAcc) {
    tallyTilt += 1;
    $("#pOnce").text(tallyTilt);
    remTime -= 1;
    // Pass data and reset our vars
    if (tallyTilt >= tallyE) {
        console.log(tallyTilt);
        passMotionData();
        motionVars();
    }
}

function passMotionData() {
    // sends it back for database handling
    var input = document.getElementById("tagVal");
    var strData = {
        'tag': input.value,
        'strAcx': JSON.stringify(acc['x']),
        'strAcy': JSON.stringify(acc['y']),
        'strTheta': JSON.stringify(rot['theta']),
        'strBeta': JSON.stringify(rot['beta']),
        'strGamma': JSON.stringify(rot['gamma'])
    }
    $.getJSON('./_balldata', strData, function() { // data
        $("#result").text("Signature received.").fadeIn().fadeOut(8000); // .text(data.ballData);
    });
};

function handleOrientation() {
    dir_a = 1;
    dir_b = 2;
    dir_g = 3;
    northFace = 4;
    document.getElementById('raws').innerHTML = [5,6,7];
    document.getElementById('compass').innerHTML = northFace;
    interval = 11;
    acc_x = 12;
    acc_y = 13;
    acc_z = 14;
    document.getElementById('accs').innerHTML = [15,16,17];
    document.getElementById('ival').innerHTML = [interval];

    for (i=0; i<5; i++) {
        ball.style.left  = 30 + "px"; //(maxX * (acc_x / 10 + 0.5) ) + "px";
        ball.style.top = 70 + "px"; //(maxY * (-acc_y / 10 + 0.5) ) + "px";
        console.log(ball.style);
        // record snapshot if we get signal
        runShaker(dir_g, Math.max(Math.abs(acc_x), Math.abs(acc_y)));
        // otherwise keep capturing data
        prettyButtons('on', remTime);
        acc['x'].push(acc_x);
        acc['y'].push(acc_y);
        // drawCanvas();
        rot['theta'].push(northFace);
        rot['beta'].push(dir_b);
        rot['gamma'].push(dir_g);
        // start tilt clock
        if (tiltStamp == 0 ) {
            tiltStamp = Date.now();
        }
        stamp = Date.now();
        playedOnce = true;
    }
}


// AND RUN
// ============================================================
$(document).on('click', '.toggle-button', function() {
    $(this).toggleClass('toggle-button-selected');
    toggler();
    if (onoff == 1) {
        motionVars();
        handleOrientation();
    }
});
setTagVal();
