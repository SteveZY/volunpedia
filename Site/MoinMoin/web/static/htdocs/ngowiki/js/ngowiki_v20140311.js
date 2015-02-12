function guid() {
    function S4() {
       return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
    }
    return (S4()+S4()+"-"+S4()+"-"+S4()+"-"+S4()+"-"+S4()+S4()+S4());
}

function getCookie( name ) { 
	var start = document.cookie.indexOf( name + "=" ); 
	var len = start + name.length + 1; 
	if ( ( !start ) && ( name != document.cookie.substring( 0, name.length ) ) ) { 
		return null; 
	} 
	if ( start == -1 ) return null; 
	var end = document.cookie.indexOf( ';', len ); 
	if ( end == -1 ) end = document.cookie.length; 
	return unescape( document.cookie.substring( len, end ) ); 
} 
function setCookie(name, value) { 
	document.cookie = name + '=' + escape( value ); 
} 

if(!getCookie('browser_user_id')) {
    setCookie('browser_user_id', guid())
}

function adjust_img_paddings() {
   if(typeof FCKeditor == 'undefined') {
		var container = $('#content');
		var containerWidth = container.width();
		var align_center_images = $('.center');
		for(var i = 0; i < align_center_images.length; i++) {
			var img = align_center_images[i];
			var imgWidth = $(img).width();
			img.style.paddingLeft = ((containerWidth - imgWidth)/2) + 'px';
		}
	} else {
		try {
			var container = $(window.frames[0].frames[0].document.body);
			var containerWidth = container.innerWidth();
			var align_center_images = $('.center', window.frames[0].frames[0].document);
			for(var i = 0; i < align_center_images.length; i++) {
				var img = align_center_images[i];
				var imgWidth = $(img).innerWidth();
				img.style.marginLeft = ((containerWidth - imgWidth)/2 - 40) + 'px';
			}
		} catch(err) {setTimeout(function(){adjust_img_paddings();}, 10);}
	}
}

$( window ).ready(function() {
    $( window ).resize ( function() {
		adjust_img_paddings();
	});
	adjust_img_paddings();
	
	$(window).scroll(function(){
		var vtop=$(document).scrollTop(),
		    vleft=$(document).scrollLeft(),
		    sidebarWidth=218,
		    topWatershed=120;
		if (vtop > topWatershed) {
			$('div.table-of-contents-float-heading').css('position', 'fixed');
			$('div.table-of-contents-float-heading').css('top', '0px');
			$('div.table-of-contents-float-heading').css('left', (sidebarWidth-vleft)+'px');
			$('div.table-of-contents').css('position', 'fixed');
			$('div.table-of-contents').css('top', '0px');
			$('div.table-of-contents').css('left', (sidebarWidth-vleft)+'px');
		} else {
			$('div.table-of-contents-float-heading').css('position', 'absolute');
			$('div.table-of-contents-float-heading').css('top', topWatershed+'px');
			$('div.table-of-contents-float-heading').css('left', sidebarWidth+'px');
			$('div.table-of-contents').css('position', 'absolute');
			$('div.table-of-contents').css('top', topWatershed+'px');
			$('div.table-of-contents').css('left', sidebarWidth+'px');
		}
	});

	if (location.search.indexOf('action=edit') != -1) {
		$(window).bind('beforeunload', function(){return '您输入的内容尚未保存，确定离开此页面吗？';});
	}

	if(typeof FCKeditor == 'undefined') {
		var attachment_images = $('.attachment');
		for(var i = 0; i < attachment_images.length; i++) {
			var img = attachment_images[i];
			var link = document.createElement('a');
			link.href = get_request_url() + '?action=viewImage&name=' + encodeURIComponent(img.getAttribute('title'));
			link.setAttribute('target', '_blank');
			img.parentNode.replaceChild(link, img);
			link.appendChild(img);
		}
	}

    var table_of_contents = $('.table-of-contents');
	for(var i = 0; i < table_of_contents.length; i++) {
	    var table_of_contents_heading = $('.table-of-contents-heading', table_of_contents[i])[0].innerHTML;
		var div = document.createElement('div');
		$(div).addClass('table-of-contents-float-heading');
		div.innerHTML = '目录';
		$(table_of_contents[i]).before(div);
		table_of_contents[i].style.display = 'none';
		
		div.__associated = table_of_contents[i];
		table_of_contents[i].__associated = div;
		$(div).click(function(){
		    $(this.__associated).fadeIn('fast');
			this.style.display = 'none';
		});
		$(table_of_contents[i]).mouseleave(function() {
		    var This = this;
		    setTimeout(function(){
			    $(This).fadeOut('fast');
				$(This.__associated).fadeIn('fast');
			}, 500)
		});
	}
	
	var discussionPanelElem = $('#page_discussion_panel');
	if(discussionPanelElem.length == 1) {
	    discussionPanelElem = discussionPanelElem[0];
	    var t = discussionPanelElem.parentNode;
		t.removeChild(discussionPanelElem);
		t.appendChild(discussionPanelElem);
		render_discussionpanel(discussionPanelElem);
	}
	
	if(!!window.__page_meta && (window.__page_meta.tags.length > 0 || window.__page_meta.locations.length > 0)) {
	    var t = $("h1", $("#page"));
		if(t.length >= 1) {
		    h1 = t[0];
			node = document.createElement("div");
			node.style.position = "relative";
			node.style.left = "-20px";
			node.style.top = "-30px";
			node.style.color = "gray";
			var ideaStatusLabel = ['活动已实现', '活动筹备中', '新创意'];
			node.innerHTML = '关键字:' + '<span style="padding-right:5px;">&nbsp;</span><a class="key-world" href=\"javascript:;\">' + [].concat(window.__page_meta.tags).concat(window.__page_meta.locations).join("</a>, <a class=\"key-world\" href=\"javascript:;\">") + "</a>" + (window.__page_meta.status !== "" ? '&nbsp; | &nbsp; 状态:<span style="padding-right:5px;">&nbsp;</span>' + ideaStatusLabel[window.__page_meta.status] : '');
			if(h1.parentNode.lastChild == h1) {
			    h1.parentNode.appendChild(node);
			} else {
			    h1.parentNode.insertBefore(node, h1.nextSibling);
			}

			$('a.key-world').click(function() {
				location.href = '/' + window.__page_meta.tags[0].substring(0, window.__page_meta.tags[0].length - 1) + '?filterByTags=' + window.__page_meta.tags[0] + ',' + $(this).text() + '&from=0';
			});
		}
	}
	
	if(!!window.__ListPagesByTag_filterByTag && !!document.getElementById("listpagesbytag_filter")) {
	    node = document.getElementById("listpagesbytag_filter");
		node.style.position = "relative";
	    node.style.left = "-15px";
		node.style.top = "-20px";
			
	    var html = "关键字：<span id='currentTags' style='margin-right:20px;display:none;'></span><div id='relatedTagsPanel' style='display:none'></div>";
		node.innerHTML = html;
		
		setTimeout(function(){
		    var t = [];
			var t2 = window.__ListPagesByTag_filterByTag.split(",");
			for(var i = 0; i < t2.length; i++) {
			    var find = false;
				for(var j = 0; j < window.__ListPagesByTag_filterByTag_default.length; j++) {
					if(t2[i] == window.__ListPagesByTag_filterByTag_default[j]) {
					    find = true;
						break;
					}
				}
				if(!find) {
				    t.push(t2[i]);
				}
			}
			if(t.length > 0) {
			    var node = document.getElementById("currentTags");
				node.style.display = '';
				for(var i = 0; i < t.length; i++) {
					var link = document.createElement("a");
					link.style.marginRight = "10px";
					link.setAttribute("href", "javascript:;");
					link.innerHTML = '<span style="padding-right:5px">' + t[i] + '</span>' + '<img src="' + window.url_prefix_static + '/ngowiki/img/icon-remove.png' + '" style="width:8px">';
					link.tag = t[i];
					$(link).on("click", function(){
						remove_filter_by_tag(this.tag);
					});
					node.appendChild(link);
				}
			}
			displayRelatedTagsPanel();
		}, 1);
	}
	
	if(!!document.getElementById("listpagesbytag_sorter")) {
	    var node = document.getElementById("listpagesbytag_sorter");
		node.innerHTML = '排序：<select id="listpagesbytag_sorter_select"><option value="lastmodified">修改时间</option><option value="likecount">推荐数</option><option value="commentcount">评论数</option><option value="hitcount">访问量</option><option value="title">名称</option></select>';
		setTimeout(function(){
		    sortby = get_query_parameter("sortby");
			if(!sortby) {
			    sortby = "lastmodified";
			}
		    $('#listpagesbytag_sorter_select')[0].value = sortby;
		    $('#listpagesbytag_sorter_select').on("change", function(){
			    var selected = $('#listpagesbytag_sorter_select')[0].value;
				var url = create_request_url(get_request_url(), get_query_parameters(), {'sortby': selected, 'from': "0"});
	            window.location.href = url;
			});
			document.getElementById("listpagesbytag_sorter").style.position = "relative";
			document.getElementById("listpagesbytag_sorter").style.top = "-20px";
			document.getElementById("listpagesbytag_sorter").style.float = "right";
		}, 1);
	}
});

function get_query_parameter(name) {
	var uri = window.location.search;
	var re = new RegExp("" +name+ "=([^&?]*)", "ig");
	return ((uri.match(re))?(uri.match(re)[0].substr(name.length+1)):null);
}

function get_query_parameters() {
    var uri = window.location.search;
	var re = new RegExp("([^&?]*)=([^&?]*)", "ig");
	return uri.match(re);
}

function get_request_url() {
    var uri = window.location.href;
	var idx = uri.indexOf("?");
	if(idx == -1) return uri;
	return uri.substring(0, idx);
}

function create_request_url(url, parameters, replace_parameters) {
    if(!parameters) parameters = [];
	
	new_parameters = []
	for(var i = 0; i < parameters.length; i++) {
	    find = false;
	    for(t in replace_parameters) {
		    if(parameters[i].indexOf(t + '=') == 0) {
			    find = true;
			}
		}
		if(!find) {
		    new_parameters.push(parameters[i]);
		}
	}
	for(t in replace_parameters) {
	    if(typeof replace_parameters[t] != 'string' || replace_parameters[t].length > 0)
	        new_parameters.push(t + '=' + replace_parameters[t]);
	}
	
	ret = url;
	for(var i = 0; i < new_parameters.length; i++) {
	    if(i == 0) {
		    ret = ret + '?';
		} else {
		    ret = ret + '&';
		}
		ret = ret + new_parameters[i];
	}
	
	return ret;
}

function render_pagingbar(total, pagesize) {
    offset = get_query_parameter('from');
	if(!offset) {
	    offset = 0;
	} else {
	    offset = parseInt(offset);
	}
	offset += 1;
	current_page = Math.ceil(offset/pagesize);
	total_page = Math.ceil(total/pagesize);
	if(pagesize >= total) {
	    return;
	}
	prev_url = '';
	next_url = '';
	prev_link = '上一页';
	next_link = '下一页';
	if(current_page > 1) {
	    prev_link = ' <a href="' + create_request_url(get_request_url(), get_query_parameters(), {'from': (current_page - 2) * pagesize}) + '">上一页</a> ';
	}
	if(current_page < total_page) {
	    next_link = ' <a href="' + create_request_url(get_request_url(), get_query_parameters(), {'from': current_page * pagesize}) + '">下一页</a> ';
	}
    document.write('<div style="padding-top:10px; padding-bottom:10px">' + ' ' + prev_link + ' ' + '<span style="padding-left:10px; padding-right:10px">第 ' + current_page + ' / ' + total_page + ' 页</span>' + ' ' + next_link + ' ' + '</div>');
}

function recommend() {
    $.ajax({url: get_request_url() + '?action=discussion&do=like&from=0&length=3&sessionId=' + getCookie('browser_user_id'), dataType: 'json', success: function(data){
	    render_discussionpanel($('#page_discussion_panel')[0], data);
	}});
}

function unrecommend() {
    $.ajax({url: get_request_url() + '?action=discussion&do=unlike&from=0&length=3&sessionId=' + getCookie('browser_user_id'), dataType: 'json', success: function(data){
	    render_discussionpanel($('#page_discussion_panel')[0], data);
	}});
}

function comment() {
    $('#discussion_comment_form')[0].style.display = '';
}

function remove_comment(commentid) {
    $.ajax({url: get_request_url() + '?action=discussion&do=removecomment&from=0&length=3&commentid=' + commentid, dataType: 'json', success: function(data){
	    render_discussionpanel($('#page_discussion_panel')[0], data);
	}});
}

function on_cancel_discussion_comment() {
    $('#discussion_comment_form')[0].style.display = 'none';
	$('#discussion_comment_content')[0].value = '';
}

function on_submit_discussion_comment() {
    $('#discussion_comment_form')[0].style.display = 'none';
	$.ajax({type: "POST", url: get_request_url() + '?action=discussion&do=comment&from=0&length=3', data: {"content": $('#discussion_comment_content')[0].value}, dataType: 'json', success: function(data){
	    $('#discussion_comment_content')[0].value = '';
	    render_discussionpanel($('#page_discussion_panel')[0], data);
	}});
}

function superrecommend() {
    $('#discussion_superrecommend_form')[0].style.display = '';
	$('#discussion_superrecommend_content')[0].value = window.__superuser_recommend_content;
}

function on_cancel_discussion_superrecommend() {
    $('#discussion_superrecommend_form')[0].style.display = 'none';
	$('#discussion_superrecommend_content')[0].value = '';
}

function on_submit_discussion_superrecommend() {
    $('#discussion_superrecommend_form')[0].style.display = 'none';
	$.ajax({type: "POST", url: get_request_url() + '?action=discussion&do=superrecommend&from=0&length=3', data: {"content": $('#discussion_superrecommend_content')[0].value}, dataType: 'json', success: function(data){
	    $('#discussion_superrecommend_content')[0].value = '';
	    render_discussionpanel($('#page_discussion_panel')[0], data);
	}});
}

Date.prototype.format = function(format) {  
	/* 
	* format="yyyy-MM-dd hh:mm:ss"; 
	*/  
	var o = {  
		"M+" : this.getMonth() + 1,  
		"d+" : this.getDate(),  
		"h+" : this.getHours(),  
		"m+" : this.getMinutes(),  
		"s+" : this.getSeconds(),  
		"q+" : Math.floor((this.getMonth() + 3) / 3),  
		"S" : this.getMilliseconds()  
	}  
	  
	if (/(y+)/.test(format)) {  
		format = format.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));  
	}  
	  
	for (var k in o) {  
		if (new RegExp("(" + k + ")").test(format)) {  
		    format = format.replace(RegExp.$1, RegExp.$1.length == 1 ? o[k] : ("00" + o[k]).substr(("" + o[k]).length));  
		}  
	}  
	return format;  
}  

function render_discussionpanel(div, data, offset, length) {
    if(!offset) offset = 0
	if(!length) length = 3
    if(!div) {
        document.write('<div id="page_discussion_panel"></div>');
    } else {
	    if(!data) {
			$.ajax({url: get_request_url() + '?action=discussion&from=' + offset + '&length=' + length + '&sessionId=' + getCookie('browser_user_id'), dataType: 'json', success: function(data){
				render_discussionpanel(div, data, offset, length);
			}});
		} else {
		    window.__superuser_recommend_content = data.superrecommend;
			
			var likemeta = false;
			if($('.likemeta').length == 0) {
				var titleH1 = $('h1', document.getElementById('page'))[0];
				likemeta = document.createElement("span");
				$(likemeta).addClass('likemeta');
				titleH1.appendChild(likemeta);
			} else {
			    likemeta = $('.likemeta')[0];
			}
			likemeta.innerHTML = data.likecount + '人喜欢';
		
		    var t = '';
			t = t + '<div style="font-size: 110%;font-family: SIMHEI;">' + data.likecount + '人喜欢 ' + ', ' + data.commentcount + '人评论' + '</div>';
			if(data.comments.items.length > 0) {
			    t = t + '<table class="discussion_panel_commentlist"><tbody>';
				for(var i = 0; i < data.comments.items.length; i++) {
				    var comment = data.comments.items[i];
					t = t + '<tr onmouseover="javascript:document.getElementById(\'delete-' + comment.id + '\').style.display=\'\'" onmouseleave="javascript:document.getElementById(\'delete-' + comment.id + '\').style.display=\'none\'">';
					t = t + '<td style="width:120px;">' + '<div style="font-weight:bolder">' + comment.user_name + '</div>' + '<div class="datemeta">' + new Date(comment.posttime * 1000).format('yyyy/MM/dd hh:mm') + '</div>' + '</td>';
					t = t + '<td><div style="width:80%;">' + comment.comment + '</div></td>';
					if(comment._delete_) {
					    t = t + '<td style="width:10px;"><a id="delete-' + comment.id + '" href="javascript:remove_comment(\'' + comment.id + '\')" style="display:none">' + 'x' + '</a></td>';
				    }
					t = t + '</tr>';
				}
				t = t + '</tbody></table>';
			}
			
			t = t + '<div style="min-height:30px">';
			if($('#logout').length == 1 || offset > 0 || length < data.commentcount || !!getCookie('browser_user_id')) {
			    t = t + '<table style="width:100%;padding:0px;margin:0px;"><tbody><tr>';
				if($('#logout').length == 1 || !!getCookie('browser_user_id')) {
					t = t + '<td style="padding:0px;margin:0px"><div style="padding-top: 20px;">';
					t = t + (!data.hasUserLikedPage ? '<a href="javascript:recommend()">我也喜欢</a>' : '<a href="javascript:unrecommend()">取消喜欢</a>');
					if($('#logout').length == 1) {
						t = t + '<span style="padding-left:5px;">&nbsp;</span>' + '<a href="javascript:comment()">我要评论</a>';
						if(!document.getElementById('page_edit_disabled')) {
							t = t + '<span style="padding-left:5px;"><a href="' + create_request_url(get_request_url(), [], {'action': 'edit', 'editor': "gui"}) + '">我要改良</a></span>';
						}
						if(data.isSuperUser) {
							t = t + '<span style="padding-left:5px;">&nbsp;</span>' + '<a href="javascript:superrecommend()">特别推荐</a>';
						}
					}
					t = t + '</div></td>';
				}
				if(offset > 0 || length < data.commentcount) {
					t = t + '<td style="padding:0px;margin:0px;text-align:right;"><div style="padding-top: 20px;">';
					if(offset == 0) {
						t = t + '<span style="padding-right:10px">' + '上一页' + '</span>';
					} else {
						_offset = offset - length;
						if(_offset < 0) _offset = 0;
						t = t + '<span style="padding-right:10px">' + '<a href="javascript:render_discussionpanel($(\'#page_discussion_panel\')[0], undefined,' + _offset + ', ' + length + ')">' + '上一页' + '</a>' + '</span>';
					}
					if(offset + length >= data.commentcount) {
						t = t + '<span style="padding-left:10px;border-left:1px solid gray;">' + '更多' + '</span>';
					} else {
						_offset = offset + length;
						t = t + '<span style="padding-left:10px;border-left:1px solid gray;">' + '<a href="javascript:render_discussionpanel($(\'#page_discussion_panel\')[0], undefined,' + _offset + ', ' + length + ')">' + '更多' + '</a>' + '</span>';
					}
					t = t + '</div></td>';
				}
				t = t + '</tr></tbody></table>';
			}
			
			t += '<div id="discussion_comment_form" style="display:none">'
			t += '<div><textarea style="border-collapse: collapse; border-spacing: 2px; border-color: #BBB; border-width: 1px; width:100%; height: 5em;" id="discussion_comment_content"></textarea></div>';
			t += '<div style="margin-top:5px;"><input type="button" name="submit" value="提交" onclick="javascript:on_submit_discussion_comment();">&nbsp;<input type="button" name="cancel" value="取消" onclick="javascript:on_cancel_discussion_comment();"></div>';
			t += '</div>';
			
			t += '<div id="discussion_superrecommend_form" style="display:none">'
			t += '<div><textarea style="border-collapse: collapse; border-spacing: 2px; border-color: #BBB; border-width: 1px; width:100%; height: 5em;" id="discussion_superrecommend_content"></textarea></div>';
			t += '<div style="margin-top:5px;"><input type="button" name="submit" value="提交" onclick="javascript:on_submit_discussion_superrecommend();">&nbsp;<input type="button" name="cancel" value="取消" onclick="javascript:on_cancel_discussion_superrecommend();"></div>';
			t += '</div>';
			
			t += '</div>';
			div.innerHTML = t;
		}
	}
}

function add_filter_by_tag(tag) {
    old_filterByTags = window.__ListPagesByTag_filterByTag;
	t = old_filterByTags.split(",")
	var find = false;
	for(i = 0; i < t.length; i++) {
	    if(t[i] == tag) find = true;
	}
	if(!find) {
	    t.push(tag);
	}
	new_filterByTags = t.join(",");
	var url = create_request_url(get_request_url(), get_query_parameters(), {'filterByTags': new_filterByTags, 'from': "0"});
	window.location.href = url;
}

function remove_filter_by_tag(tag) {
    old_filterByTags = window.__ListPagesByTag_filterByTag;
	t = old_filterByTags.split(",")
	t2 = [];
	for(i = 0; i < t.length; i++) {
	    if(t[i] != tag) t2.push(t[i]);
	}
	new_filterByTags = t2.join(",");
	if(t2.length == 0) {
	    new_filterByTags = "";
	}
	var url = create_request_url(get_request_url(), get_query_parameters(), {'filterByTags': new_filterByTags, 'from': "0"});
	window.location.href = url;
}

__displayRelatedTagsPanel__initialized = false;
function displayRelatedTagsPanel(data) {
    if(!!__displayRelatedTagsPanel__initialized) {
	    document.getElementById('relatedTagsPanel').style.display = '';
	}
    if(!data) {
		$.ajax({url: get_request_url() + '?action=relatedtags&tags=' + encodeURIComponent(window.__ListPagesByTag_filterByTag), dataType: 'json', success: function(data){
					displayRelatedTagsPanel(data);
				}});
	} else {
	    if(data.length == 0)
		    return;
			
	    var html = document.createElement("div");
		moreSpan = document.createElement("span");
		moreSpan.style.display = 'none';
		moreSpan.setAttribute("id", "relatedTagsPanel_moreitems");
	    for(var i = 0; i < data.length; i++) {
		    tag = data[i];
		    var link = document.createElement("a");
			link.setAttribute("href", "javascript:;");
			link.innerHTML = tag.tag;
			link.tag = tag.tag;
			$(link).on("click", function(){
			    add_filter_by_tag(this.tag);
			});
			if(i <= 9) {
		        html.appendChild(link);
			} else {
			    moreSpan.appendChild(link);
			}
			if(i == 9) {
				var morelink = document.createElement("a");
				morelink.id = "relatedTagsPanel_morelink";
				morelink.setAttribute("href", "javascript:;");
				morelink.innerHTML = "【更多】";
				morelink.style.borderBottom = 'none';
				$(morelink).on("click", function(){
					document.getElementById('relatedTagsPanel_moreitems').style.display = '';
					this.style.display = 'none';
				});
			    html.appendChild(morelink);
			    html.appendChild(moreSpan);
			}
			if(i > 0 && ((i % 10) == 9) && i != data.length - 1) {
			    moreSpan.appendChild(document.createElement("br"));
			}
		}
		
		{
			var lesslink = document.createElement("a");
			lesslink.setAttribute("href", "javascript:;");
			lesslink.innerHTML = "【收起】";
			lesslink.style.borderBottom = 'none';
			$(lesslink).on("click", function(){
				document.getElementById('relatedTagsPanel_moreitems').style.display = 'none';
				document.getElementById('relatedTagsPanel_morelink').style.display = '';
			});
			moreSpan.appendChild(lesslink);
		}
		
		document.getElementById('relatedTagsPanel').innerHTML = '';
		document.getElementById('relatedTagsPanel').appendChild(html);
		document.getElementById('relatedTagsPanel').style.display = '';
		
		__displayRelatedTagsPanel__initialized = true;
	}
}
