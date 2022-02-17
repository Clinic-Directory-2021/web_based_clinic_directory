function toAddItem(){
   window.location.href = '/add_item/';
}

function returnEmpty(){
   
   if(document.getElementById("edit_prod_img").files.length == 0){
      console.log("no files selected");
      return false;
  }

}

function MarkProductAvailable(key, product_img_url, product_img_old_directory,  product_name, product_price, description, category){
   $.post({
      type: 'post',
      url: "/product_item_availability/",
      data: {
          product_key: key,
          availability: "available",
          prod_name: product_name,
          prod_price: product_price,
          prod_img_url: product_img_url,
          prod_img_directory: product_img_old_directory,
          desc: description,
          categ: category,
          csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
      },
      success: function(data){
         location.reload();
      },
      error: function(data){
          alert(data + 'have an error');
      },

  });
}

function MarkProductNotAvailable(key, product_img_url, product_img_old_directory,  product_name, product_price, description, category){
   $.post({
      type: 'post',
      url: "/product_item_availability/",
      data: {
          product_key: key,
          availability: "not available",
          prod_name: product_name,
          prod_price: product_price,
          prod_img_url: product_img_url,
          prod_img_directory: product_img_old_directory,
          desc: description,
          categ: category,
          csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
      },
      success: function(data){
         location.reload();
      },
      error: function(data){
          alert(data + 'have an error');
      },

  });
}


