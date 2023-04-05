// function for autotype
function autoType(elementClass, typingSpeed, specific_class){
    var thhis = $(elementClass);
    thhis.css({
      "position": "relative",
      "display": "inline-block"
    });
    thhis.prepend('<div class="cursor" style="right: initial; left:0;"></div>');
    thhis = thhis.find(specific_class);
    var text = thhis.text().trim().split('');
    var amntOfChars = text.length;
    var newString = "";
    thhis.text("|");
    setTimeout(function(){
      thhis.css("opacity",1);
      thhis.prev().removeAttr("style");
      thhis.text("");
      for(var i = 0; i < amntOfChars; i++){
        (function(i,char){
          setTimeout(function() {        
            newString += char;
            thhis.text(newString);
          },i*typingSpeed);
        })(i+1,text[i]);
      }
    },1500);
}

// display pfp
function previewFile() {
    var preview = document.querySelector("#rect_profile_signup");
    var file    = document.querySelector('input[type=file]').files[0];
    var reader  = new FileReader();

    reader.onloadend = function () {
        preview.src = reader.result;
    }

    if (file) {
        reader.readAsDataURL(file);
        $("#text_profile_signup").css("top","506px");
    } else {
        preview.src = "";
        $("#text_profile_signup").css("top","306px");
    }
}

//auto typing
function specificType(clas,ids){
    $('.pop_up').hide();
    $(ids).show();
    autoType(".type-js",20,clas);
}

  $(document).ready(function(){
    // choosing which text to display
    $('#username_signup').focus(function(){
        specificType(".pop_signup1","#pop_sign1");
    })

    $('#email_signup').focus(function(){
        specificType(".pop_signup2","#pop_sign2");
    })

    // signup
    $('#create_account_signup').click(function(){
        // if everything is correct
        window.location.href = "{{url_for('loader3')}}";
    })
  });