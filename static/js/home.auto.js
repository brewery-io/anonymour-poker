$.ajax({
  url: Cookies.get('api') + '/room/list',
  method: 'post',
  success: function(data) {
    if (data.status == 200) {
      var rooms = data.payload.rooms
      console.log(rooms)
      for (var i = 0; i < rooms.length; i++) {
        $('#rooms_list tr:last').after('<tr ><td >' + rooms[i].name + '</td><td >' + rooms[i].seats + '</td><td >' + rooms[i].buyin + '</td><td >' + rooms[i].type + '</td><td >' + rooms[i].status + '</td></tr>')
      }
    } else {
      console.log(data)
    }
  },
  error: function(data) {
    console.log(data)
  }
})
