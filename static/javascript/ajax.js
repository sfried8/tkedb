$(document).ready(function() {

    $('#active').click(function(){
    var scroll;
    alert("Success?");
    scroll = $(this).attr("data-scroll");
    $.get('/update_active/', {brother_scroll:scroll, brother_active:$('#active').checked}, function(){
               alert("Success!");
           });
});

});