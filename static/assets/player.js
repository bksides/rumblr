var playlist = [];
playkey = -1;
var currentsong = 0;

function setAudioSource(url)
{
	player = document.getElementById('nowplaying');
	player.setAttribute('src', url);
	player.load();
	player.play();
	$("#playbutton").addClass("playing")
}

function playsong(index)
{
	$("#"+currentsong.toString()).css("background-color", "#555555");
	currentsong = index%playlist['list'].length;
	setAudioSource(playlist['list'][currentsong].audio_url);
	$("#playinfo").remove();
	$("#playercontrol").prepend($("<div id=\"playinfo\"></div>"));
	$('#playinfo').html("<img src=\""+playlist['list'][currentsong].album_art+"\" class=\"control\" id=\"coverart\"/>Title: "+playlist['list'][currentsong].track_name+"<br>Artist: "+playlist['list'][currentsong].artist+"<br>Album: "+playlist['list'][currentsong].album);
	if(reslist['key'] == playlist['key'])
	{
		$("#"+currentsong.toString()).css("background-color", "#333333");
	}
}

function skip()
{
	playsong(currentsong+1);
}

function back()
{
	if($("#nowplaying").get(0).currentTime > 3 || currentsong == 0)
	{
		$("#nowplaying").get(0).currentTime = 0;
	}
	else
	{
		playsong(currentsong-1);
	}
}

$(document).ready(function(){
	$("#playbutton").click(function(){
		if($("#nowplaying").get(0).paused && $("#nowplaying").attr('src') != null)
		{
			$("#nowplaying").get(0).play();
			$(this).addClass("playing");
		}
		else
		{
			$("#nowplaying").get(0).pause();
			$(this).removeClass("playing");
		}
	});

	$("#nowplaying").on("ended", function(){
		skip();
	});

	$("#nowplaying").on("error", function(){
		var toskip = currentsong;
		setTimeout(function(){
			if(toskip == currentsong)
			{
				skip();
			}
		}, 1500);
		$("#playinfo").text("Player error; skipping");
	});

	$("#nextbutton").click(function(){
		skip();
	});

	$("#backbutton").click(function(){
		back();
	});
});