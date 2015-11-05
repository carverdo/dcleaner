// Defines Function and Calls (producing return)
// ============================================================
getL();

function getL() {
    // Init Controller
    var controller = new ScrollMagic.Controller();

    //create a new Scene
    var scene = new ScrollMagic.Scene({
        triggerElement: "#pinned-trigger1",
        duration: 1200, //pin the #pinned-trigger1 element for 1200px
        //of scrolling
        triggerHook:"onLeave", //trigger:onLeave = trigger
        //animation when the top of triggerElement hits top of viewport
        //in this case, animation is "setPin"
        reverse:true})
        .setPin("#pinned-element1")
        .addTo(controller);

    var scene2 = new ScrollMagic.Scene({
        triggerElement: "#pinned-trigger2",
        duration:700,
        triggerHook:"onLeave",
        reverse:true})
        .setPin("#pinned-element2")
        .addTo(controller);
}


