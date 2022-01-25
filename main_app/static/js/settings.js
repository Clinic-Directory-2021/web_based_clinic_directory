var edit = document.getElementById("settings_edit");
var save = document.getElementById("settings_save");
var credentials = document.getElementsByClassName("credentials");
save.style.display = "none";



$('#map').hide();
function edit_clinic_info(){
    $('#map').show();

   for(i = 0; i < credentials.length; i++)
   {
        credentials[i].disabled = false;
        credentials[5].disabled = true;
        credentials[6].disabled = true;
        credentials[7].disabled = true;
   }

   $('#opening_time').prop('disabled', false);
   $('#closing_time').prop('disabled', false);
  
   edit.style.display = "none";
   save.style.display = "block";

}

$('#settingsForm').on('submit', function(e){
    $('#loader').show();

    var formData = new FormData();
    var files = $('#clinic_image')[0].files[0];
  
    formData.append('clinicImage', files);
    formData.append('fileName', files.name);
    
    formData.append('old_image_directory', credentials[0].value);
    formData.append('editClinicName', credentials[2].value);
    formData.append('editClinicAddress', credentials[3].value);
    formData.append('clinicContact', credentials[4].value);
    formData.append('editLatitude', credentials[5].value);
    formData.append('editLongitude', credentials[6].value);
    formData.append('opening_time', tConvert($('#opening_time').val()));
    formData.append('closing_time', tConvert($('#closing_time').val()));
    formData.append('editClinicDescription', credentials[8].value);
    formData.append('csrfmiddlewaretoken', $("input[name='csrfmiddlewaretoken']").val());
    e.preventDefault();
    console.log("1");
    $.ajax({
        type: 'post',
        url: "/save_clinic_info/",
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        data: formData,
        success: function(data){
            $('#loader').hide();
            //$('#responseMessage').html(data);
            $('#map').hide();

            edit.style.display = "block";
            save.style.display = "none";
            for(i = 0; i < credentials.length; i++)
                {
                        credentials[i].disabled = true;
                }

                $('#opening_time').prop('disabled', true);
                $('#closing_time').prop('disabled', true);

            if(data == 'Information Updated Successfully!'){
                Swal.fire({
                    position: 'middle',
                    icon: 'success',
                    title: 'Information Updated Successfully!',
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




  var iframe = document.getElementsByTagName("iframe")[0];

  var mapClick = iframe.contentWindow.document.getElementsByTagName("div")[0];

  var elmnt = iframe.contentWindow.document.getElementsByClassName("leaflet-popup-content-wrapper")[0];

  setInterval(function(){ 
        elmnt = iframe.contentWindow.document.getElementsByClassName("leaflet-popup-content-wrapper")[0];
        try{
          elmnt = elmnt.textContent.replace(/[^\d.-]/g, '');

          elmnt = elmnt.substring(0, 7) + "*" + elmnt.substring(7, elmnt.length);
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