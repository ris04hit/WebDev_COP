// display post
function post_display(){
    var photo_exist = true;
    var zip_filename = "filename";
    if (photo_exist) {
        var size = parseInt($('#text_post4').height()) + 1000;
        $("#image_inside_post").show();
        $("#image_inside_post").css('top', size - 600);
    }
    else{
        var size = parseInt($('#text_post4').height()) + 503;
    }
    $("#zip_name_post").html(zip_filename);
    $("#zip_name_post").css('top', size+20);
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