$(".leave_btn").click(function() {
	$.ajax({
		url: "http://localhost:8080/game/action",
		method: "post",
		data: {
			"sesh": localStorage.getItem("sesh"),
			"action": "leave",
			"game_id": localStorage.getItem("game_id")
		},
		success: function(data) {
			console.log(data);
		},
		error: function(error) {
			console.log(error);
		}
	});
});
