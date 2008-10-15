$(function(){
    $('#id_upload').after(' <a href="#" id="photo-edit">Edit this photo</a>');
    $('#photo-edit').hide();
    var ext = '';
    //check if the upload field contains an image path or PDF
    $('#id_upload').change(function(){
        var image_ext = ['.jpg', '.jpeg', '.gif', '.png', '.pdf'];
        var found = false;
        for (var i=0; i<image_ext.length; i++) {
            if ($(this).val().lastIndexOf(image_ext[i]) > 0) {
                found = true;
                ext = image_ext[i].replace('.','');
                break;
            }
        }
        if (found == true)
            $('#photo-edit').show();
        else
            $('#photo-edit').hide();
    });
    //edit form to post to snipshot and submit
    $('a#photo-edit').click(function(){
        $(this).after('<input type="hidden" name="snipshot_input" value="upload"/>');
        $(this).after('<input type="hidden" name="snipshot_callback" value="'+document.location.href+'"/>');
        $(this).parents('form').attr('action', 'http://services.snipshot.com/');
        $(this).parents('form').submit();
        return false;
    });
});