var next_url = "home.html"
// var search_list = ["taaag1", "tffag2","aatag3"];
function updateFileName() {
  const fileName = document.getElementById('zip-upload_Devang').files[0].name;
  document.getElementById('selected-file').textContent = fileName;
}
function updateFileName2() {
  const fileName = document.getElementById('Image-upload_Devang').files[0].name;
  document.getElementById('selected-file2').textContent = fileName;
}

function hideImage(img) {
  img.style.display = 'none';
}

$(function(){
    $("#header").load("{{url_for('header')}}"); 
  });


  // tag pop up
  // function search_click() {
  //     if (search_list.length){
  //       $("#search_result_rect").show();
  //     }
  //     var rect_ht = 50 + 41*search_list.length;
  //     $("#search_result_rect").css("height",rect_ht.toString().concat("px"));
  //     var html = "";
  //     var top = -13;
  //     for (var count=0; count< search_list.length; count++){
  //         top = top + 41;
  //         var code = `<div id = "search_text-${count}" class="text4" style = "top : ${top}px; left : 29px">${search_list[count]}</div><rect class="search_line header_search_line" style = "top : ${top+30}px; width : 220px"></rect>`
  //         html = html.concat(code);
  //       }
  //     console.log(html);
  //     $("#search_result_rect").html(html);
  //   }

$(document).ready(function(){
    var href = document.location.href;
    var lastPathSegment = href.substr(href.lastIndexOf('/') + 1);
    if (lastPathSegment === "{{url_for('signup')}}"){
        $("#not_show_signup").hide();
    }
    // window.print("kksf klsdlk lkkfsm ")
    // print("TIkTIk")
    $('#rect_search').on('input', function() {
      var query = $('#rect_search').val();
      // window.print("tollksplks")
      $.ajax({
          url: '/search',
          method: 'POST',
          data: {'query': query},
          success: function(response) {
              var search_list = response.results;
              var id_uniqs = response.id_uniqs;
              var renderes = response.renderes;
              // var html = '';
              if (search_list.length){
                $("#search_result_rect").show();
              }
              var rect_ht = 50 + 41*search_list.length;
              if (search_list.length > 10){
                rect_ht = 460;
              }
              $("#search_result_rect").css("height",rect_ht.toString().concat("px"));
              var html = "";
              var top = -13;
              for (var count=0; count< search_list.length && count < 10; count++){
                  top = top + 41;
                  var code = `<a href="{{url_for('profile', username='__id__')}}"><div id = "search_text-${count}" class="text4" style = "top : ${top}px; left : 29px; overflow-x: hidden; overflow-y : hidden; height : 30px">${search_list[count]}</div></a><rect class="search_line header_search_line" style = "top : ${top+30}px; width : 220px; overflow-x: hidden; overflow-y : hidden"></rect>`
                  code = code.replace('__id__', id_uniqs[count]);
                  code = code.replace('profile', renderes[count]);
                  html = html.concat(code);
                }
              // console.log(html);

              $("#search_result_rect").html(html);
              // for (var i = 0; i < results.length && i < 10; i++) {
              //     var row = results[i];
              //     html += '<p>' + row + '</p>';
              // }
              // $('#results').html(html);
          }
      });
  });
  $('#inp_home1').on('input', function() {
    var query = $('#inp_home1').val();
    // window.print("tollksplks")
    $.ajax({
        url: '/searchPost',
        method: 'POST',
        data: {'query': query},
        success: function(response) {
            var search_list = response.results;
            var id_uniqs = response.id_uniqs;
            // var html = '';
            if (search_list.length){
              $("#searchPost_result_rect").show();
            }
            console.log(search_list)
            var rect_ht = 50 + 41*search_list.length;
            if (search_list.length > 10){
              rect_ht = 460;
            }
            $("#searchPost_result_rect").css("height",rect_ht.toString().concat("px"));
            var html = "";
            var top = -13;
            for (var count=0; count< search_list.length && count < 10; count++){
                top = top + 41;
                var code = `<a href="{{url_for('post', post_id='__id__')}}"><div id = "search_text-${count}" class="text4" style = "top : ${top}px; left : 29px; overflow-x: hidden; overflow-y : hidden">
                ${search_list[count]}
                </div></a>
                <rect class="search_line header_search_line" style = "top : ${top+30}px; width : 500px; overflow-x: hidden; overflow-y : hidden"></rect>`
                code = code.replace('__id__', id_uniqs[count]);
                html = html.concat(code);
              }
            // console.log(html);
            $("#searchPost_result_rect").html(html);
            // for (var i = 0; i < results.length && i < 10; i++) {
            //     var row = results[i];
            //     html += '<p>' + row + '</p>';
            // }
            // $('#results').html(html);
        }
    });
});
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
          setTimeout(function() {
            $("#search_result_rect").empty().hide();
        }, 50);
      })

      $("#inp_home1").focus(function(){
        search_click();
        $("#searchPost_result_rect").show();
      })
      $("#inp_home1").blur(function(){
        setTimeout(function() {
            $("#searchPost_result_rect").empty().hide();
        }, 50);
    });
})