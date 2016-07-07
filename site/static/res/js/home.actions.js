$(document).on("click", ".room", function() {
	var room_id = $(this).attr("room-id");

	$.ajax({
		url: "http://localhost:8080/room/join",
		method: "post",
		data: {
			"sesh": localStorage.getItem("sesh"),
			"room_id": room_id
		},
		success: function(data) {
			if (data["status"] == 200) {
				localStorage.setItem("room_id", data["payload"]["room_id"]);
				if (data["payload"]["started"]) {
					localStorage.setItem("game_id", data["payload"]["game_id"]);
					localStorage.setItem("state_id", 0);
					window.location="/game"
				} else {
					window.location="/room"
				}
			} else {
				console.log(data);
			}
		},
		error: function(error) {
			console.log(error);
		}
	});
});
$(".logout_btn").click(function() {
	$.ajax({
		url: "http://localhost:8080/user/logout",
		method: "post",
		data: {
			"sesh": localStorage.getItem("sesh")
		},
		success: function(data) {
			localStorage.removeItem("sesh");
			window.location="/login";
		},
		error: function(error) {
			console.log(error);
		}
	})
});
