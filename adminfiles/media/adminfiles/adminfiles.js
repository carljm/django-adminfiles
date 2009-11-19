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

//change the following 3 functions to insert HTML, Markdown, whatever
function buildImage(image_url, alt_text, width, height, align, link, use_html) {
    textile = ' !';
    markdown = ' ![';
    html = '<img ';
    if (align == 'left') {
        textile += '<';
        markdown += '{@class=left}';
        html += 'class="left" align="left" ';
    }
    else if (align == 'right') {
        textile += '>';
	markdown += '{@class=right}';
        html += 'class="right" align="right"';
    }
    markdown += '{@width=' + width + '}{@height=' + height + '}';
    textile += image_url + '(' + alt_text + ')!';
    markdown += alt_text + '](' + image_url + ')';
    html += 'src="'+image_url+'" alt="'+alt_text+'" />';
    if (link) {
        textile += ':' + link;
        markdown = '[' + markdown + '](' + link + ')';
        html = '<a href="'+link+'">'+html+'</a>';
    }
    if (use_html)
        return html + ' ';
    else
        return markdown + ' ';
}
//this needs some help via a templatetag
function buildVideoLink(video_url, title, thumb, use_html) {
    if (use_html)
        return '<a class="flash_video" href="'+video_url+'" title="'+title+'"><img src="'+thumb+'" alt="'+title+'" /></a>';
    return '\n\n&& flash_video ' + video_url + ' &&\n\n';
}

function buildLink(link_url, title, use_html) {
    if (use_html)
        return ' <a href="'+link_url+'" title="'+title+'">'+title+'</a> ';
    textile = ' "'+title+'":'+link_url+' ';
    markdown = ' [' + title + '](' + link_url + ') ';
    return markdown;
}



$(function(){
    $('#adminfiles li').click(function(){
	    $(this).children('.popup').show();
	});
    $('.popup .close').click(function(){
	    $(this).parent('.popup').hide();
	    return false;
	});
    $('.popup .select').click(function(){
	    for (i=0; i<FIELD.options.length; i++) {
		if (FIELD.options[i].value == this.rel) { FIELD.options[i].selected = true; }
	    }
	    $(this).parents('.popup').hide();
	    return false;
	});
    $('.popup .insert').click(function(){
            var use_html = false;
	    var title = $(this).attr('title');
	    if ($(this).parents('.image').length) {
		var rel = $(this).attr('rel').split(':');
		var link = $(this).parents('li').siblings('li.link').children('input.link').val();
		var code = buildImage(this.href, title, rel[0], rel[1], rel[2], link, use_html);
	    }
	    else if ($(this).parents('.youtube').length) {
		var code = buildVideoLink(this.href, title, this.rel, use_html);
	    }
	    else {
		var code = buildLink(this.href, title, use_html);
	    }

            insertAtCursor(FIELD, code);
	    $(this).parents('.popup').hide();
	    return false;
	});
    $('#refresh').click(function(){
	    location.reload(true);
	    return false;
	});
});
