jQuery.noConflict();

jQuery(document).ready(function ($) {
    $('#save_btn').on('click', function () {
        var annos = anno.getAnnotations();
        for (var i=0; i<annos.length; i++) {
            console.log(annos[i]);
        }
    });

    $(document).on('mouseup', function () {
        $('.annotorious-editor-text').val($("input:radio[name=label]:checked").val());
    });

    $(document).keypress(function(e){
        // onPress button 1
        if (e.keyCode == 49) {
            $('input:radio[name=label][value=person]').attr('checked', false);
            $('input:radio[name=label][value=car]').attr('checked', true);
        } else if (e.keyCode == 50) {
            $('input:radio[name=label][value=car]').attr('checked', false);
            $('input:radio[name=label][value=person]').attr('checked', true);
        }
    });
});
