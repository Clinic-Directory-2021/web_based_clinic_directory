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
  e.preventDefault();
  console.log("1");
  $.ajax({
      type: 'post',
      url: "/register_user_firebase/",
      data: {
        fname: $('#fname').val(),
        lname: $('#lname').val(),
        email: $('#registerEmail').val(),
        password: $('#password').val(),
        confirm_password: $('#confirm_password').val(),
        csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
        },
      success: function(data){
          $('#responseMessage').html(data);
      },
      error: function(data){
          alert('have an error');
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
