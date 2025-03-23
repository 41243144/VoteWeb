function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/profile/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.length > 0) {
            document.getElementById('studient_id').value = data[0].studient_id;
            document.getElementById('name').value = data[0].name;
            document.getElementById('form-title').innerText = '更改個人資料';
        } else {
            document.getElementById('form-title').innerText = '創建個人資料';
        }
    })
    .catch(error => console.error('Error:', error));


    var profileForm = document.getElementById('profile-form');
    if (profileForm) {
        profileForm.addEventListener('submit', function(event) {
            event.preventDefault();
            var form = event.target;
            var formData = {
                studient_id: form.studient_id.value,
                name: form.name.value
            };

            let method = 'POST';
            let url = '/api/profile/';
            if (document.getElementById('form-title').innerText === '更改個人資料') {
                method = 'PUT';
                url = '/api/profile/' + form.studient_id.value + '/';
            }

            fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.studient_id && data.name) {
                    Swal.fire({
                        icon: 'success',
                        title: '資料已成功更新',
                        showConfirmButton: false,
                        timer: 1500
                    });
                    document.getElementById('form-title').innerText = '更改個人資料';
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: '更新失敗',
                        html: '<ul>' + Object.values(data).map(function(error) {
                            return '<li>' + error + '</li>';
                        }).join('') + '</ul>',
                    });
                }
            });
        });
    }
});