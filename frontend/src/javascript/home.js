var tag_list = ["tag1", "tag2","tag3","tag4"];

// tag pop up
function tag_click() {
    $("#tag_pop_home").show();
    var rect_ht = 56 + 52*tag_list.length;
    $("#rect_tag_home").css("height",rect_ht.toString().concat("px"));
    var html = "";
    var top = 4;
    for (var count=0; count< tag_list.length; count++){
        top = top + 52;
        var code = "<a href='tag.html'>\n\t<button class='buttons_tag_home' style='top:".concat(top);
        code = code.concat("px'>");
        code = code.concat(tag_list[count]);
        code = code.concat("</button>\n</a>\n");
        html = html.concat(code);
    }
    $("#button_tag_home").html(html);
}

function upvote(post_id) {
    var up_id = "#".concat(post_id).concat(" .upvote");
    var upv = $(up_id).text();
    var upv_int = parseInt(upv);
    // if check already not upvoted then
    upv_int = upv_int + 1;
    $(up_id).html("".concat(upv_int));
}

$(document).ready(function(){
    $("#button_home2").click(function(){
        tag_click();
    })

    $(".close_pop").click(function(){
        $("#tag_pop_home").hide(1000);
    })

    // hover tag
    $("#button_home2").hover(function(){
        $("#text_home5").css("color","rgba(250, 0, 255, 0.809443)");
    }, function(){
        $("#text_home5").css("color","#FFFFFF");
    })

    // hover sort
    $("#button_home3").hover(function(){
        $("#text_home6").css("color","rgba(250, 0, 255, 0.809443)");
    }, function(){
        $("#text_home6").css("color","#FFFFFF");
    })

    // sort click
    $("#button_home3").click(function(){
        $("#sort_pop_home").show();
    })

    // hover by time
    $("#button_sort_home1").hover(function(){
        $("#text_sort_home1").css("color","#6DD6CF");
    }, function(){
        $("#text_sort_home1").css("color","#FFFFFF");
    })

    //hover by upvote
    $("#button_sort_home2").hover(function(){
        $("#text_sort_home2").css("color","#6DD6CF");
    }, function(){
        $("#text_sort_home2").css("color","#FFFFFF");
    })

    //click by time
    $("#button_sort_home1").click(function(){
        $("#rect_time_home").show();
        $("#rect_up_home").hide();
        $("#sort_pop_home").hide();
    })

    //click by upvote
    $("#button_sort_home2").click(function(){
        $("#rect_up_home").show();
        $("#rect_time_home").hide();
        $("#sort_pop_home").hide();
    })

    //hover profile
    $(".post_author").hover(function(){
        $(".post_author .text1").css("color","#03001C");
    }, function(){
        $(".post_author .text1").css("color","#FFFFFF");
    })

    //hover follow
    $(".follow").hover(function(){
        $(".follow").css("color","#00FFFF");
    }, function(){
        $(".follow").css("color","#008DFF");
    })

    //click upvote triangle
    $(".triangle-up").click(function(){
        var par = $(this).parent().attr('id');
        upvote(par);
    })
})