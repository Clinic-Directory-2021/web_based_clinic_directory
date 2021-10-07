function show_menu(){
    $('.menu-list').show();
}
function close_menu(){
    $('.menu-list').hide();
}
function showModal(){
    $('.item-modal').show();
    $('.grey').show();
    
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
