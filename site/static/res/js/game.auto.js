localStorage.setItem("state_id", 0);

function getTimeRemaining(endtime) {
	var t = Date.parse(endtime) - Date.parse(new Date());
 	var seconds = Math.floor((t / 1000) % 60);
 // 	var minutes = Math.floor((t / 1000 / 60) % 60);
	// var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
	// var days = Math.floor(t / (1000 * 60 * 60 * 24));
	return {
		'total': t,
		// 'days': days,
		// 'hours': hours,
		// 'minutes': minutes,
		'seconds': seconds
	};
}

function initializeClock(id, endtime) {
	var clock = document.getElementById(id);
	// var daysSpan = clock.querySelector('.days');
	// var hoursSpan = clock.querySelector('.hours');
	// var minutesSpan = clock.querySelector('.minutes');
	var secondsSpan = clock.querySelector('.seconds');

function updateClock() {
	var t = getTimeRemaining(endtime);

	//daysSpan.innerHTML = t.days;
	//hoursSpan.innerHTML = ('0' + t.hours).slice(-2);
	//minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
	secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);

	if (t.total <= 0) {
	  clearInterval(timeinterval);
	}
}

updateClock();
	var timeinterval = setInterval(updateClock, 1000);
}

var deadline = new Date(Date.parse(new Date()) + 15 * 24 * 60 * 60 * 1000);

var update_state = function() {
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

					$(".hand").html("<div class=\"card\" >\
									" + data["payload"]["hand"][0]["name"] + " \
									of \
									" + data["payload"]["hand"][0]["suit"] + " \
									</div>\
									<div class=\"card\" >\
									" + data["payload"]["hand"][1]["name"] + " \
									of \
									" + data["payload"]["hand"][1]["suit"] + " \
									</div>");

					$(".big").html(data["payload"]["big"]);
					$(".small").html(data["payload"]["small"]);

					console.log(localStorage.getItem("user_id"));
					console.log(data["payload"]["next_id"]);

					if (data["payload"]["next_id"] == localStorage.getItem("user_id")) {
						$(".controls").show();
						$(".timer").show();
						initializeClock('.timer', data["payload"]["expiry"]);

					} else {
						$(".controls").hide();
						$(".timer").hide();
					}

					$(".users").html("<tr ><td >player id</td><td >player action</td><td >player bet</td><td >player money</td></tr>");
					for (var i = 0; i < data["payload"]["user_ids"].length; i++) {

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
}

update_state();
setInterval(update_state, 5000);
