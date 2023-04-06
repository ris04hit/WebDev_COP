$(document).ready(function(){
    // Get Started
    $("#button_start1").click(function(){
        var left = $(document).outerWidth() - $(window).width();
        $('body, html').animate({
            scrollLeft: left
        })
    });

    // Login
    // $("#button_start2").click(function(){
    //     $("input").val("");
    //     // if (id password matches)
    //         window.location.href="{{url_for('loader1')}}";
    // })

    // forgot password
    $("#text_start7").click(function(){
        $("#forgot_start").show();

    })

    // close forgot password
    $("#close_pop_start").click(function(){
        $("#forgot_start").hide();
    })

    // login forgot password
    $("#button_start4").click(function(){
        $("input").val("");
        // if (id password matches)
            window.location.href="{{url_for('loader1')}}";
    })

    //hover forgot
    $("#text_start7").hover(function(){
        $("#text_start7").css("color","rgba(250, 0, 255, 0.809443)");
    }, function(){
        $("#text_start7").css("color","#3300FF");
    })
});