/**
 * Created by phoen on 2016/10/4.
 */
function moveSidebarDiv(){
    // windowHeight = $(window).height();
    // divHeight = $('#leftSidebar').height();
    windowWidth = $(window).width();
    divWidth = $('#leftSidebar').width();
    // var offsetTop = (windowHeight - divHeight)/2;
    var offsetLeft = windowWidth - divWidth;
    $('#leftSidebar').offset({top:50 ,left:offsetLeft});
}


