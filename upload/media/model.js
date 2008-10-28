if (typeof TinyMCE_Engine=='function') {
    tinyMCE.init({
       theme : 'django',
       theme_django_toolbar_location : 'top',
       theme_django_buttons1 : 'bold, italic, separator, bullist, numlist, outdent, indent, separator, justifyleft, justifycenter, justifyright, separator, link, unlink, separator, pastetext, pasteword, selectall',
       theme_django_buttons2 : '',
       theme_django_buttons3 : '',
       plugins : 'inlinepopups, paste',
       button_tile_map : true,
       fix_list_elements : true,
   	   gecko_spellcheck : true,
   	   verify_html : true,
   	   dialog_type : "modal",
   	   height : '300',
       mode : 'none' 
    });
}
$(function(){
    $('textarea').each(function(){
        //exclude common plain text fields
        if (!this.id.match('excerpt') && !this.id.match('teaser') && !this.id.match('comment') && !this.id.match('mission')) {
            $(this).after('<iframe frameborder="0" style="border:none; width:755px; height:210px;" src="/uploads/?textarea='+this.id+'"></iframe>');
            if (typeof TinyMCE_Engine=='function')
                tinyMCE.execCommand("mceAddControl", true, this.id); 
            //toggle WYSIWYG mode
            //tinyMCE.execCommand("mceToggleEditor", true, this.id);
        }
    });
});
