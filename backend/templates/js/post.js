// display post
function post_display(){
    var size = parseInt($('#text_post4').height()) + 403;
    $('#inner_post_post').css('height', size);
    var top = 117 + size;
    $('#footer_post_div').css('top', top);
    var top = 183 + size;
    $('#rect_comment_post').css('top', top);
    $('#line_comment_post').css('top', top+50);
    $('#add_comment_post').css('top', top+7);
    $('#button_post_0').css('top', top+13);
}

$(document).ready(function(){
    post_display();
})