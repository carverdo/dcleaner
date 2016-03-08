/*
XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
*/
function buildEle(tex) {
    newEle = $("<h2 class=css-typing>");
    newEle.text(tex);
    return newEle;
}
function slowAppend(container, text) {
    container.delay(1600).queue(function (next) {
        $(this).append(buildEle(text));
        next();
    });
}
$(document).ready(function() {
    slowAppend($("#cont"), '1. Place file in our magic directory.');
    slowAppend($("#cont"), '2. Open webpage to inspect the file; make sure it looks like it is the right "shape".');
    slowAppend($("#cont"), '3. Assert your type choices (or load previous Stamps).');
    slowAppend($("#cont"), '4. Stamp your type choices as many times as you wish.');
    slowAppend($("#cont"), '11. Assert your values OR mark as No Idea.');
    slowAppend($("#cont"), '12. Log your value assertions (name, time, suggested edit).');
});
