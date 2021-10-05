function toHomepage(){
  window.location.href = '/homepage/';
}


 var current_number_of_items = $('#current_number_of_items').val();

 var next_number_of_items = parseInt(current_number_of_items) + 1;

 var new_field_name = "item_" + next_number_of_items;

 $('#new_field_name').val(new_field_name);

 $(function(){
  $('#product_image').change(function(){
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
 
$('#add_item_form').on('submit', function(e){
  $('#loader').show();
});

/*
 var current_number_of_items = $('#current_number_of_items').val();

 var next_number_of_items = parseInt(current_number_of_items) + 1;

 var new_field_name = "item_" + next_number_of_items;

 var selected_product_image, image_fileName ;

 document.getElementById("product_image").addEventListener("change", function(e) {
    
    selected_product_image = e.target.files;
 
    //Loops through all the selected files
    for (let i = 0; i < selected_product_image.length; i++) {
    image_fileName = selected_product_image[i].name;
    }
 });

 $('#addItemForm').on('submit', function(e){
    e.preventDefault();
    console.log("1");
    $.ajax({
        type: 'post',
        url: "/add_item_firebase/",
        data: {
          product_name: $('#product_name').val(),
          product_price: $('#product_price').val(),
          field_name: new_field_name,
          product_image: selected_product_image,
          img_fileName: image_fileName,
          csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
          },
        success: function(data){
            window.location.href = '/homepage/';
        },
        error: function(data){
            alert('have an error');
        }
  
    });
  });

  */