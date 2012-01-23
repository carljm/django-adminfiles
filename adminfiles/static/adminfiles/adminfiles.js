function insertAtCursor(myField, myValue) {
    //IE support
    if (document.selection) {
        myField.focus();
        sel = document.selection.createRange();
        sel.text = myValue;
    }
    //MOZILLA/NETSCAPE support
    else if (myField.selectionStart || myField.selectionStart == '0') {
        var startPos = myField.selectionStart;
        var endPos = myField.selectionEnd;
        myField.value = myField.value.substring(0, startPos)
        + myValue
        + myField.value.substring(endPos, myField.value.length);
    } else {
        myField.value += myValue;
    }
}

function showEditPopup(triggeringLink) {
    var name = 'edit_popup';
    var href = triggeringLink.href;
    if (href.indexOf('?') == -1) {
        href += '?_popup=1';
    } else {
        href  += '&_popup=1';
    }
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

function dismissEditPopup(win) {
    location.reload(true);
    win.close();
}

function showAddUploadPopup(triggeringLink) {
    var name = 'add_upload_popup';
    var href = triggeringLink.href;
    if (href.indexOf('?') == -1) {
        href += '?_popup=1';
    } else {
        href  += '&_popup=1';
    }
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

function dismissAddUploadPopup(win) {
    location.reload(true);
    win.close();
}

$(function(){
      $('#adminfiles li').click(
          function(){
	      $(this).children('.popup').show();
	  });
      $('.popup .close').click(
          function(){
	      $(this).parent('.popup').hide();
	      return false;
	  });
      $('.popup .select').click(
          function(){
	      for (i=0; i<FIELD.options.length; i++) {
		  if (FIELD.options[i].value == this.rel) {
                      FIELD.options[i].selected = true;
                  }
	      }
	      $(this).parents('.popup').hide();
	      return false;
	  });
      $('.popup .insert').click(
          function(){
              var insertText = this.rel;
              if(!insertText.match('://')) {
                  insertText = START + insertText + END;
                  }
              insertAtCursor(FIELD, insertText);
	      $(this).parents('.popup').hide();
	      return false;
	});
    $('#refresh').click(function(){
	    location.reload(true);
	    return false;
	});
});
