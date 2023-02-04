'use strict';
(function(w,d,$){
$(d).ready(function(){
  $("div[class*='mega-menu-container-']").hide();
      $("body").on("click", "[id^='mega-menu-']", function(e){
        let id = $(this).attr('id').split("-")[2];
        console.info(id);
        console.info("class:not(mega-menu-container-"+id+")");
        $("div[class*='mega-menu-container-']").not(".mega-menu-container-"+id+"").hide();
        $(".mega-menu-container-"+id+"").fadeToggle("slow");
        return false;
      })
})/* document ready */
})(window,document,jQuery)
