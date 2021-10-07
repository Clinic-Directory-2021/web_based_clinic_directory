function show_menu(){
    $('.menu-list').show();
}
function close_menu(){
    $('.menu-list').hide();
}
function showModal(clinic_name, img_url, clinic_address){
    $('.item-modal').show();
    $('.grey').show();

    $("#item-modal-img").attr("src",img_url);

    $('#item-modal-name').text(clinic_name);

    $('#item-modal-address').text(clinic_address);
    
}

if($('.item-modal:visible').length == 0)
{
    $('.grey').click(function (event) 
    {
       
           if(!$(event.target).closest('.item-modal').length && !$(event.target).is('.item-modal')) {
             $(".item-modal").hide();
             $(".grey").hide();
           }     
    });
}
else{
    
}
