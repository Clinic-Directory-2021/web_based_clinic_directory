var edit = document.getElementById("settings_edit");
var save = document.getElementById("settings_save");
var credentials = document.getElementsByClassName("credentials");
save.style.display = "none";


function edit_clinic_info(){


   for(i = 0; i < credentials.length; i++)
   {
        credentials[i].disabled = false;
        credentials[2].disabled = true;
   }
   
  
   edit.style.display = "none";
   save.style.display = "block";

}

$('#settingsForm').on('submit', function(e){
    e.preventDefault();
    console.log("1");
    $.ajax({
        type: 'post',
        url: "/save_clinic_info/",
        data: {
          editClinicName: credentials[0].value,
          editClinicAddress: credentials[1].value,
          editClinicDescription: credentials[3].value,
          csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
          },
        success: function(data){
            $('#responseMessage').html(data);

            edit.style.display = "block";
            save.style.display = "none";
            for(i = 0; i < credentials.length; i++)
                {
                        credentials[i].disabled = true;
                }

        },
        error: function(data){
            alert('have an error');
        }
  
    });
  });