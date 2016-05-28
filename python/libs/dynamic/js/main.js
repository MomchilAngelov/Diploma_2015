$(document).ready(function(){
	"uses strict";

	function buttonClicked(){
		var name = $("[name='gameName']").val();
		var file = $("[name='gameFile']").prop("files")[0];
		var extension = file.name.split(".")[1];
		var size = file.size;
		if (extension != "py"){
			return;
		}
		if (size > 1000000){
			return;
		}

		var fd = new FormData();
		fd.append('file',file);

		var _url = "libs/dynamic/php/post_game.php"+"?Name="+name;
		var createPromise = $.ajax({
			url: _url,
			data: fd,
			dataType: "JSON",
			processData: false,
			contentType: false,
			method: "POST",
		}).then(function(responce){
			if (responce == "1"){
				$("#forms").fadeOut("slow");
				$("#forms").html("");
				$("#forms").html("<p class='no-top left big'>Game uploaded correctly! Waiting for our approval</p>");
				$("#forms").fadeIn("slow");
			}
		}).fail(function(responce){
			console.log(responce);
		});
	}

	function attachHandlers(){
		$("button").on("click", function(){
			buttonClicked();
		});
	}

	attachHandlers();
});