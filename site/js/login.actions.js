$('.register').submit(function (e) {
  e.preventDefault()
  $.ajax({
    url: 'http://localhost:8080/user/register',
    type: 'post',
    data: {
      'username': $('.register input[name=\'username\']').val(),
      'password': $('.register input[name=\'password\']').val()
    },
    success: function(data) {
      if (data['status'] === 200) {
        alert('success')
      }
    },
    error: function(error) {
      console.log(error)
    }
  })
})
$('.login').submit(function (e) {
  e.preventDefault()
  $.ajax({
    url: 'http://localhost:8080/user/login',
    type: 'post',
    data: {
      'username': $('.login input[name=\'username\']').val(),
      'password': $('.login input[name=\'password\']').val()
    },
    success: function (data) {
      if (data['status'] === 200) {
        localStorage.setItem('sesh', data['payload']['sesh'])
        localStorage.setItem('user_id', data['payload']['user_id'])
        window.location = '/'
      }
      else {
        alert(data['payload']['error'])
      }
    },
    error: function (error) {
      console.log(error)
    }
  })
})
