$('#loading').hide();

function show_menu(){
    $('.menu-list').show();
}
function close_menu(){
    $('.menu-list').hide();
}
function showModal(clinic_name, img_url, clinic_address, clicked_id){
    $('.item-modal').show();
    $('.grey').show();

    $('#loading').show();

    $("#item-modal-img").attr("src",img_url);

    $('#item-modal-name').text(clinic_name);

    $('#item-modal-address').text(clinic_address);


    formId = '#' + clicked_id;
    $('#id_field').val(clicked_id)

    
    $.post({
        type: 'post',
        url: "",
        data: {
            user_id_post: $('#id_field').val(),
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
        },
        success: function(data){
            

        },
        error: function(data){
            alert(data + 'have an error');
        },

    })
    .done(function(data){
        //console.log(data);
        $('#loading').hide();
        $('.available-item').append(data);
    });



    // $('#indexForm').submit(function (e){
    //     e.preventDefault();
    //     console.log("1");
    //     $.post({
    //         type: 'post',
    //         url: "/getItemData/",
    //         data: {
    //             user_id_post: $('#id_field').val(),
    //             csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
    //         },
    //         success: function(data){
                

    //         },
    //         error: function(data){
    //             alert(data + 'have an error');
    //         },
    
    //     })
    //     .done(function(data){
    //         data = JSON.parse(data);
    //         console.log(data["item_1"]['product_price'])
    //         return;
    //     });
    // })

        //$('#indexForm').submit();


}

if($('.item-modal:visible').length == 0)
{
    $('.grey').click(function (event) 
    {
       
           if(!$(event.target).closest('.item-modal').length && !$(event.target).is('.item-modal')) {
             $(".item-modal").hide();
             $(".grey").hide();
             	
             $( ".item" ).remove();
           }     
    });
}
else{
    
}
