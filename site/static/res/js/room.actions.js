$(".leave_room").click(function() {
	$.ajax({
		method: "post",
		url: "http://localhost:8080/room/leave",
		data: {
			"sesh": localStorage.getItem("sesh")
		},
		success: function(data) {
			if (data["status"] == 200) {
				localStorage.removeItem("room_id");
				location.href="/";
			} else {
				alert(data["payload"]["error"]);
			}
		},
		error: function(error) {
			console.log(error);
		}
	})
});
