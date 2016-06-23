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
			if (data["status"] == 200) {
				console.log(data);
				localStorage.removeItem("sesh");
				window.location="/login";
			} else {
				console.log(data);
			}
		},
		error: function(error) {
			console.log(error);
		}
	})
});
