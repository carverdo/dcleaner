/*
XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
*/
/* =========================
RUN OUR FUNCTION
========================= */
$(document).ready(function() {
    buttonPush();
});
/* =========================
SIMPLE BIND EVENTS
========================= */
function buttonPush() {
    var fname = $('#fname');
    var prevRes = localStorage.getItem('fname');
    if (prevRes) {fname.val(prevRes);};
    // handling_buttons
    $('#grabber').click(function(e) {
        var tmp = fname.val();
        localStorage.setItem('fname', tmp);
    });
}
