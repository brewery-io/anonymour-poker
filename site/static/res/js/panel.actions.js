$('.create_room').submit(function (e) {
  e.preventDefault()
  $.ajax({
    url: 'http://localhost:8080/room/create',
    type: 'post',
    data: {
      'sesh': localStorage.getItem('sesh'),
      'name': $('.create_room input[name=\'name\']').val(),
      'max_players': $('.create_room input[name=\'max_players\']').val(),
      'buyin': $('.create_room input[name=\'buyin\']').val()
    },
    success: function (data) {
      console.log(data)
    },
    error: function (error) {
      console.log(error)
    }
  })
})
