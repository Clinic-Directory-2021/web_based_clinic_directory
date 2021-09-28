function toAddItem(){
   window.location.href = '/add_item/';
}

function returnEmpty(){
   
   if(document.getElementById("edit_prod_img").files.length == 0){
      console.log("no files selected");
      return false;
  }

}