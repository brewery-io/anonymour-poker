setInterval(function() {
	$.ajax({
		method: "post",
		url: "http://localhost:8080/game/state",
		data: {
			"sesh": localStorage.getItem("sesh"),
			"state_id": localStorage.getItem("state_id"),
			"game_id": localStorage.getItem("game_id"),
		},
		success: function(data) {
			if (data["status"] == 200) {
				if (data["payload"]["changed"]) {
					localStorage.setItem("state_id", data["payload"]["id"]);
					console.log(data);
					var community = "";
					for (var i = 0; i < data["payload"]["community"].length; i++) {
						community += "<div class='card' >" + data["payload"]["community"][i]["name"] + ", " + data["payload"]["community"][i]["suit"] + "</div>"
					}
					$(".community").html(community);

					for (var i = 0; i < data["payload"]["user_ids"].length; i++) {
						console.log(i);
						$(".users").append("<tr >\
							<td > \
								" + data["payload"]["user_ids"][i] + "\
							</td >\
							<td > \
								" + data["payload"]["actions"][data["payload"]["user_ids"][i]] + "\
							</td >\
							<td > \
								" + data["payload"]["bets"][data["payload"]["user_ids"][i]] + "\
							</td >\
							<td > \
								" + data["payload"]["money"][data["payload"]["user_ids"][i]] + "\
							</td >\
						</tr>")
					}

				}
			} else {
				alert(data["payload"]["error"]);
			}
		},
		error: function(error) {
			console.log(error);
		}
	});
}, 5000);
