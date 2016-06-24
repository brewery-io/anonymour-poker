setInterval(function() {
	$.ajax({
		method: "post",
		url: "http://localhost:8080/room/status",
		data: {
			"room_id": localStorage.getItem("room_id")
		},
		success: function(data) {
			if (data["status"] == 200) {
				if (data["payload"]["ingame"]) {
					localStorage.setItem("game_id", data["payload"]["game_id"]);
					localStorage.setItem("state_id", 0);
					//location.href="/game";
					window.location = "/game"
				}
			} else {
				console.log(data);
			}
		},
		error: function(error) {
			console.log(error);
		}
	})
}, 2000);
