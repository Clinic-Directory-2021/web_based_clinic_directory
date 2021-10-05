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
        credentials[4].disabled = true;
        credentials[5].disabled = true;
        credentials[6].disabled = true;
   }
   
  
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
    formData.append('editLatitude', credentials[4].value);
    formData.append('editLongitude', credentials[5].value);
    formData.append('editClinicDescription', credentials[7].value);
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
            $('#responseMessage').html(data);

            edit.style.display = "block";
            save.style.display = "none";
            for(i = 0; i < credentials.length; i++)
                {
                        credentials[i].disabled = true;
                }

        },
        error: function(data){
            $('#loader').hide();
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