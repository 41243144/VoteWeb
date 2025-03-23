document.addEventListener('DOMContentLoaded', function() {
    var input = document.querySelector('input[name=tags]');
    var categorySelect = document.getElementById('category');
    var submitButton = document.querySelector('#article-form button[type=submit]');
    var isSubmitting = false;

    const postId = document.getElementById('article-form').dataset.postId;

    fetch(`/api/post/${postId}/detail/`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            document.getElementById('title').value = data.title;
            document.getElementById('content').value = data.content;
            document.getElementById('link').value = data.link;
            document.getElementById('category').value = data.category;
            
            if (data.tags) {
                tagify.addTags(data.tags); // 使用 tagify.addTags 設置標籤
            }

            fetch('/api/category/')
                .then(response => response.json())
                .then(categories => {
                    categories.results.forEach(function(category) {
                        var option = document.createElement('option');
                        option.value = category.id;
                        option.textContent = category.name;
                        if (category.name === data.category) {
                            option.selected = true;
                        }
                        categorySelect.appendChild(option);

                        
                    });
                })
                .catch(error => console.error('獲取類別資料時出錯：', error));
        })
        .catch(error => console.error('Error fetching article data:', error));

    // 初始化 Tagify
    var tagify = new Tagify(input, {
        whitelist: [], // 初始為空，稍後通過 AJAX 獲取
        maxTags: 5,
        dropdown: {
            maxItems: 3,           // 最大顯示數量
            classname: "tags-look", // 自定義樣式
            enabled: 0,             // 0: focus時顯示, 1: 輸入時顯示
            closeOnSelect: true,    // 選擇後不關閉下拉選單
        },
        originalInputValueFormat: valuesArr => valuesArr.map(item => item.value)
    });

    tagify.on("add", function(e) {
        if (e.detail.data.value.length > 10) {
            tagify.removeTag(e.detail.tag);
            Swal.fire({
                title: '錯誤',
                text: '標籤長度不能超過 10 個字符！',
                icon: 'error',
                confirmButtonText: '確定'
            });
        }
    });

    // 獲取標籤資料
    fetch('/api/tag/')
        .then(response => response.json())
        .then(data => {
            tagify.settings.whitelist = data.results.map(tag => tag.name);
        })
        .catch(error => console.error('獲取標籤資料時出錯：', error));

    // // 獲取類別資料
    // fetch('/api/category/')
    //     .then(response => response.json())
    //     .then(data => {
    //         data.results.forEach(function(category) {
    //             console.log(category);
    //             var option = document.createElement('option');
    //             option.value = category.id;
    //             option.textContent = category.name;
    //             categorySelect.appendChild(option);
    //         });
    //     })
    //     .catch(error => console.error('獲取類別資料時出錯：', error));

    // 獲取 CSRF Token
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

    // 表單提交處理
    document.getElementById('article-form').addEventListener('submit', function(event) {
        event.preventDefault(); 

        if (isSubmitting) return;
        isSubmitting = true;
        var formData = new FormData(this);

        submitButton.disabled = true;

        fetch(`/api/post/${postId}/update/`, {
            method: 'PUT',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(errorData.detail || '發布文章時出錯');
                });
            }
            return response.json();
        })
        .then(data => {
            // 成功送出文章
            Swal.fire({
                title: '成功',
                text: '文章已成功更新！',
                icon: 'success',
                confirmButtonText: '確定'
            });
            // 清空表單
            document.getElementById('article-form').reset();
            tagify.removeAllTags();
            // 重新啟用提交按鈕
            submitButton.disabled = false;
            isSubmitting = false; // 重置提交狀態
        })
        .catch(error => {
            // 錯誤訊息
            Swal.fire({
                title: '錯誤',
                text: error.message,
                icon: 'error',
                confirmButtonText: '確定'
            });
            // 重新啟用提交按鈕
            submitButton.disabled = false;
            isSubmitting = false; // 重置提交狀態
        });
    });
});