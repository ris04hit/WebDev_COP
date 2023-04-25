var next_url = "home.html"
var search_list = ["taaag1", "tffag2","aatag3","taggg4"];

$(function(){
    $("#header").load("{{url_for('header')}}"); 
  });


  // tag pop up
  function search_click() {
      if (search_list.length){
        $("#search_result_rect").show();
      }
      var rect_ht = 50 + 41*search_list.length;
      $("#search_result_rect").css("height",rect_ht.toString().concat("px"));
      var html = "";
      var top = -13;
      for (var count=0; count< search_list.length; count++){
          top = top + 41;
          var code = `<div id = "search_text-${count}" class="text4" style = "top : ${top}px; left : 29px">${search_list[count]}</div><rect class="search_line header_search_line" style = "top : ${top+30}px; width : 220px"></rect>`
          html = html.concat(code);
        }
      console.log(html);
      $("#search_result_rect").html(html);
    }

$(document).ready(function(){
    var href = document.location.href;
    var lastPathSegment = href.substr(href.lastIndexOf('/') + 1);
    if (lastPathSegment === "{{url_for('signup')}}"){
        $("#not_show_signup").hide();
    }

    $("#rect_home, #home").hover(function(){
        $("#rect_home").css("background-color", "#B6EADA");
        $("#home").css("color", "#03001C");
        }, function(){
        $("#rect_home").css("background-color", "#03001C");
        $("#home").css("color", "#FFFFFF");
      });

      $("#rect_about, #about").hover(function(){
        $("#rect_about").css("background-color", "#B6EADA");
        $("#about").css("color", "#03001C");
        }, function(){
        $("#rect_about").css("background-color", "#03001C");
        $("#about").css("color", "#FFFFFF");
      });

      $("#rect_apis, #apis").hover(function(){
        $("#rect_apis").css("background-color", "#B6EADA");
        $("#apis").css("color", "#03001C");
        }, function(){
        $("#rect_apis").css("background-color", "#03001C");
        $("#apis").css("color", "#FFFFFF");
      });

      $("#profile_rect, #profile_photo, #profile_name").hover(function(){
        $("#profile_rect").css("background-color", "#8F00FF");
        }, function(){
        $("#profile_rect").css("background-color", "#03001C");
      });      

      $(".close_pop").hover(function(){
        $(this).css("color", "#FFFAFA");
      }, function(){
        $(this).css("color", "#7F7F7F");
      })

      $("#rect_search").focus(function(){
        search_click();
        $("#search_result_rect").show();
      })

      $("#rect_search").blur(function(){
        $("#search_result_rect").hide();
      })
})