$(document).ready(function(){
    $(".rect_option_profile").hover(function(){
        $(this).css("background","rgba(250, 0, 255, 0.809443)");
    }, function(){
        $(this).css("background","#03001C");
    })
    
    $("#history_profile").hover(function(){
        $("#rect_option_profile1").css("background","rgba(250, 0, 255, 0.809443)");
    }, function(){
        $("#rect_option_profile1").css("background","#03001C");
    })  
    
    $("#setting_profile").hover(function(){
        $("#rect_option_profile2").css("background","rgba(250, 0, 255, 0.809443)");
    }, function(){
        $("#rect_option_profile2").css("background","#03001C");
    })  
    
    $("#bookmark_profile").hover(function(){
        $("#rect_option_profile3").css("background","rgba(250, 0, 255, 0.809443)");
    }, function(){
        $("#rect_option_profile3").css("background","#03001C");
    })  
    
    $("#insti_profile").hover(function(){
        $("#rect_option_profile4").css("background","rgba(250, 0, 255, 0.809443)");
    }, function(){
        $("#rect_option_profile4").css("background","#03001C");
    })  
    
    $("#following_profile").hover(function(){
        $("#rect_option_profile5").css("background","rgba(250, 0, 255, 0.809443)");
    }, function(){
        $("#rect_option_profile5").css("background","#03001C");
    })  
    
    $("#follower_profile").hover(function(){
        $("#rect_option_profile6").css("background","rgba(250, 0, 255, 0.809443)");
    }, function(){
        $("#rect_option_profile6").css("background","#03001C");
    })  

    $("#rect_option_profile5").click(function(){
        $("#following_pop").show(300);
    })
    $("#close_following").click(function(){
        $("#following_pop").hide(200);
    })

    $("#rect_option_profile6").click(function(){
        $("#followers_pop").show(300);
    })
    $("#close_followers").click(function(){
        $("#followers_pop").hide(200);
    })

    $("#rect_option_profile4").click(function(){
        $("#Insti_popup").show(300);
    })
    $("#close_ins").click(function(){
        $("#Insti_popup").hide(200);
    })

    $("#rect_option_profile2").click(function(){
        $("#rect_main_set").show(300);
    })
})