(function($){
  $(document).ready(function(){
    $(".tasks").sortable({
      connectWith: ".tasks",
      placeholder: ".on_tasks",
      helper: function( event ) {
        return $("<div class='elem_move'>moving...</div>");
      },
      scroll: false,
      cursorAt: { top: 25, left: 30}
    });
  });
})(jQuery);
