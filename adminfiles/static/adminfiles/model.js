(function($) {
     $(function(){
           $('.adminfilespicker').each(
               function(){
	           var href = '/adminfiles/all/?field='+this.id;
	           if (this.options) {
		       $(this).siblings('a.add-another').remove();
		       href += '&field_type=select';
	           }
	           $(this).after('<iframe frameborder="0" style="border:none; width:755px; height:210px;" src="' + href + '"></iframe>');
	       });
       });
 })(jQuery);
