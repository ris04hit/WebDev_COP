var next_url = "home.html"

$(function(){
    $("#header").load("{{url_for('header')}}"); 
  });

$(document).ready(function(){
    var href = document.location.href;
    var lastPathSegment = href.substr(href.lastIndexOf('/') + 1);
    if (lastPathSegment === "{{url_for('signup')}}"){
        $("#not_show_signup").hide();
    }

    $("#rect_home, #home").hover(function(){
        $("#rect_home").css("background-color", "#B6EADA");
        }, function(){
        $("#rect_home").css("background-color", "#03001C");
      });

      $("#rect_about, #about").hover(function(){
        $("#rect_about").css("background-color", "#B6EADA");
        }, function(){
        $("#rect_about").css("background-color", "#03001C");
      });

      $("#rect_apis, #apis").hover(function(){
        $("#rect_apis").css("background-color", "#B6EADA");
        }, function(){
        $("#rect_apis").css("background-color", "#03001C");
      });

      $("#profile_rect, #profile_photo, #profile_name").hover(function(){
        $("#profile_rect").css("background-color", "#8F00FF");
        }, function(){
        $("#profile_rect").css("background-color", "#03001C");
      });      
})