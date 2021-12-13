function showBookAppointment(){
    clinic_id_appointment = $('#item-modal-user-id').text();
    $('#user_id_appointment').val(clinic_id_appointment);
    window.console.log("Hello world");
    console.log("APPOINTMENT!!!!!!!");
}

// $('#loading').hide();
// $( ".search-modal" ).hide();

// setInterval(function(){ 
//     if(!$("#searchItem").is(":focus")){
//         $( ".search-result" ).remove();
//         $( ".search-modal" ).hide();
//     }

// }, 
// 1000);




function show_menu(){
    $('.menu-list').show();
}
function close_menu(){
    $('.menu-list').hide();
}

$('#search-clinic-form').on('submit', function(e){
    e.preventDefault();
    $( ".preview-item" ).remove();
    console.log("1");
    $.ajax({
        type: 'post',
        url: "/search_clinic/",
        data: {
            search_item: $('#searchItem').val(),
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
          },
        success: function(data){
            $( ".preview-item" ).remove();
            $('.preview').append(data);
        },
        error: function(data){
            alert('have an error');
        },
  
    });
});




function suggestSearch(){
    $( ".search-result" ).remove();
    $( ".search-modal" ).show();

        if( $('#searchItem').val() == ""){
            $( ".search-result" ).remove();
            $( ".search-modal" ).hide();
        }
        else{
            $.post({
                type: 'post',
                url: "/getSearchData/",
                data: {
                    search_item: $('#searchItem').val(),
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                },
                success: function(data){
                $( ".search-result" ).remove();

                },
                error: function(data){
                    alert(data + 'have an error');
                },

            })
            .done(function(data){
                $('.search-modal').append(data);

                notFound = "<p class=\"search-not-found\"> Not Found! </p>";
                if($('.search-result').length)
                {
                    $( ".search-not-found" ).remove();
                }
                else{
                    $( ".search-not-found" ).remove();
                    $('.search-modal').append(notFound);
                }
            });
        }

}

function showModal(clinic_name, img_url, clinic_address, clicked_id , clinic_description, opening, closing,number){
    $('.item-modal').show();
    $('.grey').show();

    $('#loading').show();

    $("#item-modal-img").attr("src",img_url);

    $('#item-modal-name').text(clinic_name);

    $('#item-modal-address').text(clinic_address);

    $('#item-modal-description').text(clinic_description);
    
    $('#item-modal-closingHours').text(opening + ' - ' + closing);

    $('#item-modal-contact').text(number);

    $('#item-modal-user-id').text(clicked_id);
    
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
        $( ".item" ).remove();
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



