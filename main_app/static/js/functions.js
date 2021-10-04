//Email Address validation for registration of user
function validation(){
    var form = document.getElementById('registerForm');
    var email = document.getElementById('registerEmail').value;
    var text = document.getElementById('emailValidationText');
    var pattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

    if(email.match(pattern)){
        form.classList.add("valid");
        form.classList.remove("invalid");
        text.innerHTML = "Your Email Address is Valid";
        text.style.color = "#00ff00";
    }
    else{
        form.classList.remove("valid");
        form.classList.add("invalid");
        text.innerHTML = "Please Enter Valid Email Address";
        text.style.color = "#ff0000";
    }

}

$('#registerForm').on('submit', function(e){

  var formData = new FormData();
  var files = $('#clinic_image')[0].files[0];

  formData.append('clinicImage', files);
  formData.append('fileName', files.name);
  formData.append('clinicName', $('#clinicName').val());
  formData.append('clinicAddress', $('#clinicAddress').val());
  formData.append('latitude', $('#latitude').val());
  formData.append('longitude', $('#longitude').val());
  formData.append('clinicDescription', $('#clinicDescription').val());
  formData.append('email', $('#registerEmail').val());
  formData.append('password', $('#password').val());
  formData.append('confirm_password', $('#confirm_password').val());
  formData.append('csrfmiddlewaretoken', $("input[name='csrfmiddlewaretoken']").val());


  e.preventDefault();
  console.log("1");
  $.ajax({
      type: 'post',
      url: "/register_user_firebase/",
      enctype: 'multipart/form-data',
      processData: false,
      contentType: false,
      data: formData,
      success: function(data){
          $('#responseMessage').html(data);
      },
      error: function(data){
          alert(data + 'have an error');
      }

  });
});

$('#loginForm').on('submit', function(e){
    e.preventDefault();
    console.log("1");
    $.ajax({
        type: 'post',
        url: "/login_validation/",
        data: {
          login_email: $('#login_email').val(),
          login_password: $('#login_password').val(),
          csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
          },
        success: function(data){
            if(data=="Invalid Email or Password!"){
                 $('#responseMessage').html(data);
            }else{
              location.reload();
            }
        },
        error: function(data){
            alert('have an error');
        }
  
    });
  });

  var iframe = document.getElementsByTagName("iframe")[0];

  var mapClick = iframe.contentWindow.document.getElementsByTagName("div")[0];

  var elmnt = iframe.contentWindow.document.getElementsByClassName("leaflet-popup-content-wrapper")[0];

  setInterval(function(){ 
        elmnt = iframe.contentWindow.document.getElementsByClassName("leaflet-popup-content-wrapper")[0];
        try{
            const coordinates = elmnt.textContent.split("*");

            $('#latitude').val(coordinates[0]);
            $('#longitude').val(coordinates[1]);
        }
        catch(e){
            $('#latitude').val("");
            $('#longitude').val("");
        }
    }, 
    100);

    $(function(){
        $('#clinic_image').change(function(){
          var input = this;
          var url = $(this).val();
          var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
          if (input.files && input.files[0]&& (ext == "png" || ext == "jpeg" || ext == "jpg")) 
           {
              var reader = new FileReader();
      
              reader.onload = function (e) {
                 $('#preview_img').attr('src', e.target.result);
              }
             reader.readAsDataURL(input.files[0]);
          }
          else
          {
            $('#preview_img').attr('src', '../static/images/map.jpg');
          }
        });
      
      });
    
    

//   mapClick.addEventListener("click", myFunction);

//  function myFunction() {
//    if( elmnt == undefined)
//    {
 
//     elmnt = iframe.contentWindow.document.getElementsByClassName("leaflet-popup-content-wrapper")[0];
//    }
   

   
//     alert(elmnt.textContent);
   
   
// }


  
