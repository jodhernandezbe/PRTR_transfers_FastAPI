/* DataTable */

$(document).ready( function () {
    $('#my_table').DataTable();
    } );

/* View in fullscreen */
function openFullscreen(id) {
    var elem = document.getElementById(id);
    if (elem.requestFullscreen) {
    elem.requestFullscreen();
    } else if (elem.webkitRequestFullscreen) { /* Safari */
    elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) { /* IE11 */
    elem.msRequestFullscreen();
    }
}


if ( window.location.pathname == '/' ){
    if ($(window).width() > 768){
        var height = $(window).height() - ($("#header").outerHeight() + $("#footer").outerHeight());
    } else {
        var height =  0.6*($("#header").outerHeight() + $("#footer").outerHeight());
    }
    $("#main").css("height",height+"px");
    $(".carousel-inner img").css("height",height+"px");
    $(".carousel-inner").css("height",height+"px");
    $(".carousel").css("height",height+"px");
    var width = $(window).width();
    $("#main").css("width",width+"px");
    $(".carousel-inner img").css("width",width+"px");
    $(".carousel-inner").css("width",width+"px");
    $(".carousel").css("width",width+"px");
};