
//Email Address validation for registration of user
function validation(){
    var form = document.getElementById('registerForm');
    var email = document.getElementById('registerEmail').value;
    var text = document.getElementById('emailValidationText');
    var pattern = /^[^ ]+@gmail+\.com$/;

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
  $('#loader').show();
  var formData = new FormData();
  var files = $('#clinic_image')[0].files[0];

  formData.append('clinicImage', files);
  formData.append('fileName', files.name);
  formData.append('clinicName', $('#clinicName').val());
  formData.append('clinicAddress', $('#clinicAddress').val());
  formData.append('clinicContact', $('#clinicContact').val());
  formData.append('latitude', $('#latitude').val());
  formData.append('longitude', $('#longitude').val());
  formData.append('clinicDescription', $('#clinicDescription').val());
  formData.append('email', $('#registerEmail').val());
  formData.append('password', $('#password').val());
  formData.append('confirm_password', $('#confirm_password').val());
  formData.append('opening_time', tConvert($('#opening_time').val()));
  formData.append('closing_time', tConvert($('#closing_time').val()));
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
          $('#loader').hide();
        //   $('#responseMessage').html(data);
        
          if(data == 'Email Already Exists!'){
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: data,
              })
          }
          else if(data == 'Password Do not Match!'){
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: data,
              })
          }
          else if(data == 'New User Registered Successfully!'){
            Swal.fire({
                position: 'middle',
                icon: 'success',
                title: 'Your Request Have Been Successfully Sent!',
                text: 'Please wait for Email Confirmation if your Request will be Accepted or Declined, Confirmation Will Be sent to Your Provided Email!',
                showConfirmButton: true,
                confirmButtonText: 'PROCEED',
              }).then((result) => {
                if (result.isConfirmed) {
                    location.reload();
                }
              })
          }else if(data == 'Time Error'){
            Swal.fire({
              icon: 'error',
              title: 'Oops...',
              text: "Opening Time Can't be Later than Closing Time!",
            })
          }

      },
      error: function(data){
          $('#loader').hide();
          Swal.fire({
                icon: 'error',
                title: 'Oops...',
              })
      }

  });
});

$('#loginForm').on('submit', function(e){
    $('#loader').show();
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
            $('#loader').hide();
            if(data=="Invalid Email or Password!"){
                //  $('#responseMessage').html(data);
                 Swal.fire({
                    icon: 'error',
                    title: data,
                    confirmButtonText: 'OKAY',
                  })
            }else if (data == 'Success!'){
                $('#loader').hide();
                Swal.fire({
                    position: 'middle',
                    icon: 'success',
                    title: 'Login Successful!',
                    showConfirmButton: true,
                    confirmButtonText: 'PROCEED',
                  }).then((result) => {
                    if (result.isConfirmed) {
                        location.reload();
                    }
                  })
            }
        },
        error: function(data){
            $('#loader').hide();
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
              })
        },
  
    });
  });

  var iframe = document.getElementsByTagName("iframe")[0];

  var mapClick = iframe.contentWindow.document.getElementsByTagName("div")[0];

  var elmnt = iframe.contentWindow.document.getElementsByClassName("leaflet-popup-content-wrapper")[0];

  setInterval(function(){ 
        elmnt = iframe.contentWindow.document.getElementsByClassName("leaflet-popup-content-wrapper")[0];

        
        try{
          elmnt = elmnt.textContent.replace(/[^\d.-]/g, '');

          elmnt = elmnt.substring(0, 7) + "*" + elmnt.substring(7, elmnt.length);
            const coordinates = elmnt.split("*");

            $('#latitude').val(coordinates[0]);
            $('#longitude').val(coordinates[1]);
        }
        catch(e){
            $('#latitude').val("");
            $('#longitude').val("");     
        }
    }, 
    100);

    function tConvert(time) {
        // Check correct time format and split into components
        time = time.toString().match(/^([01]\d|2[0-3])(:)([0-5]\d)(:[0-5]\d)?$/) || [time];
    
        if (time.length > 1) { // If time format correct
          time = time.slice(1); // Remove full string match value
          time[5] = +time[0] < 12 ? ' AM' : ' PM'; // Set AM/PM
          time[0] = +time[0] % 12 || 12; // Adjust hours
        }
        return time.join(''); // return adjusted time or original string
      }


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


  
