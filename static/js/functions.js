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


$(window).resize(function() {
    if ( document.URL.includes("") ){
        var height = $(window).height() - ($("#header").outerHeight(true) + $("#footer").outerHeight(true));
        $("#main").css("min-height",height+"px");
        // $(".carousel-inner img").css("min-height",height+"px");
    }
});


$(function(){
    $(document).ready(function(){
        var height = $(window).height();
var header =$('header.site-navbar').height();
var finalheight =height-header;
// alert(finalwidth);
$('.carousel-item img').css('height',''+finalheight+'px');
});
    });
