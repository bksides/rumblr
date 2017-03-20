var reslist = {};
var allreslists = [];
var reskey = 0;

function search(blog, tag, callback)
{
	$("#results").remove();
	$("#loading").remove();
	$(".content").append($("<p id=\"loading\">Loading...</p>"));
	$.ajax({
		url: "/query/search?blog="+encodeURIComponent(blog)+"&tag="+encodeURIComponent(tag),
		type: "GET",
		success: function(data){
			reslist = {'key': reskey, 'list': JSON.parse(data)};
			allreslists[reskey] = reslist;
			callback(reslist);
			reskey++;
		},
		error: function(data){
			reslist = null;
			callback(null);
		},
		timeout: 20000
	});
}

function putResults(res)
{
	$("#results").remove();
	$("#loading").remove();
	if(res != null && res['list'] != null && res['list'].length > 0)
	{
		$(".content").append($("<div id=\"results\"></div>"));
		$("#results").perfectScrollbar({theme: 'rumblr'});
		for(result in res['list'])
		{
			$("#results").append($("<div class=\"resdiv\" id=\""+result+"\">\n\
				<img class=\"thumbnail\" src=\""+res['list'][result].album_art+"\"/>\n\
				Title: "+res['list'][result].track_name+"<br>\n\
				Artist: "+res['list'][result].artist+"<br>\n\
				Album: "+res['list'][result].album+"<br>\n\
				</div>\n\
				<hr>\n"));
			$("#"+result).click(function(){
				playlist=reslist;
				playsong(parseInt($(this).attr('id')));
			});
		}
	}
	else
	{
		$(".content").append($("<p id=\"loading\"></p>"));
		$("#loading").text('No results found.');
	}
}

function newSearchResults(res)
{
	putResults(res);
	window.history.pushState({'reslist': reslist['key'], 'blog': $("#blog").get(0).value, 'tag': $("#tag").get(0).value}, "", "/search?blog="+$("#blog").get(0).value+"&tag="+$("#tag").get(0).value);
}

$(document).ready(function(){
	$("#searchbutton").click(function(event){
		event.preventDefault();
		search($("#blog").get(0).value,$("#tag").get(0).value, newSearchResults);
	});

	window.onpopstate=function(event){
		reslist = allreslists[event.state['reslist']];
		putResults(reslist);
		$("#tag").get(0).value = event.state['tag'];
		$("#blog").get(0).value = event.state['blog'];
		if(reslist['key']==playlist['key'])
		{
			$("#"+currentsong.toString()).css("background-color", "#333333");
		}
	};
});