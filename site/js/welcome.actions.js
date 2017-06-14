$('#register_btn').click(function (e) {
  e.preventDefault()
  $.ajax({
    url: Cookies.get('api') + '/user/register',
    type: 'post',
    data: {
      'username': $('#register_form > input[name="username"]').val(),
      'password': $('#register_form > input[name="password"]').val()
    },
    success: function(data) {
      if (data['status'] == 200) {
        console.log('success')
      }
    },
    error: function(error) {
      console.log(error)
    }
  })
})

$('#login_btn').click(function (e) {
  e.preventDefault()
  $.ajax({
    url: Cookies.get('api') + '/user/login',
    type: 'post',
    data: {
      'username': $('#login_form > input[name="username"]').val(),
      'password': $('#login_form > input[name="password"]').val()
    },
    success: function (data) {
      if (data.status == 200) {
        Cookies.set('token', data.payload.token)
        window.location.reload()
      } else {
        console.log(data.payload.message)
      }
    },
    error: function (error) {
      console.log(error)
    }
  })
})
