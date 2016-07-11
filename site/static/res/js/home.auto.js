$.ajax({
  url: 'http://localhost:8080/room/list',
  method: 'post',
  success: function (data) {
    if (data['status'] == 200) {
      for (var i = 0; i < data['payload']['rooms'].length; i++) {
        $('.roomslist tr:last').after('<tr class=\'room\' room-id=\'\'' + data['payload']['rooms'][i][0] + '> \
          <td > ' + data['payload']['rooms'][i][1] + ' \
          </td> \
          <td > ' + data['payload']['rooms'][i][2] + ' \
          </td> \
          <td > ' + data['payload']['rooms'][i][3] + ' \
          </td> \
          <td > ' + data['payload']['rooms'][i][4] + ' \
          </td> \
          <tr/>');
      }
    } else {
      console.log(data)
    }
  },
  error: function (error) {
    console.log(error)
  }
})
