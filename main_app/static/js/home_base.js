function dashboard(){
    window.location.href = '/homepage';
}
function show_menu(){
    $('.menu-list').show();
}
function close_menu(){
    $('.menu-list').hide();
}


function appointmentDecline(appointment_id, appointment_name,appointment_email, appointment_date, appointment_time){
    Swal.fire({
        title: 'Type your Reason Why The Appointment is Declined',
        input: 'textarea'
      }).then(function(result) {
        if (result.value) {
          $('#loader').show();
            $.ajax({
                type: 'post',
                url: "/declineAppointment/",
                data: {
                    appointment_id: appointment_id,
                    name: appointment_name,
                    email: appointment_email,
                    date: appointment_date,
                    time: appointment_time,
                    reasons: result.value,
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                    },
                success: function(data){
                    location.reload();
                    $('#loader').hide();
                }, 
                error: function(data){
                    $('#loader').hide();
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                      })
                },
          
            });
        }
      })
}