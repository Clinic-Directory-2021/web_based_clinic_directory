var default_img_src;

function editItem(key , product_img_url, product_img_old_directory,  product_name, product_price){
    
    default_img_src = product_img_url;

    $('#edit_prod_img_preview').attr('src', product_img_url);

    $('#edit_prod_name').val(product_name);
    $('#edit_prod_price').val(product_price);
    $('#edit_field_name').val(key);

    $('#old_image_directory').val(product_img_old_directory);
    
    console.log(key);
}

$(function(){
    $('#edit_prod_img').change(function(){
      var input = this;
      var url = $(this).val();
      var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
      if (input.files && input.files[0]&& (ext == "png" || ext == "jpeg" || ext == "jpg")) 
       {
          var reader = new FileReader();
  
          reader.onload = function (e) {
             $('#edit_prod_img_preview').attr('src', e.target.result);
          }
         reader.readAsDataURL(input.files[0]);
      }
      else
      {
        $('#edit_prod_img_preview').attr('src', default_img_src);
      }
    });
  
  });

  $('#edit_item_form').on('submit', function(e){
    $('#loader').show();
  });