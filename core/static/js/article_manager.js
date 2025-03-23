// filepath: e:\programing\python\django\MinecraftWeb\MinecraftServer\core\static\js\article_manager.js
let currentPage = 1;
let totalPages = 1;

function fetchArticles(page) {
    if (page < 1 || page > totalPages) return;
    fetch(`/api/post/details/?page=${page}`)
        .then(response => response.json())
        .then(data => {
            console.log('Fetched data:', data);
            const articlesContainer = document.getElementById('articles-container');
            articlesContainer.innerHTML = '';
            data.results.forEach(post => {
                const articleHTML = `
                    <div class="col-lg-6 col-md-6 mb-5">
                        <div class="blog-item">
                            <div class="blog-item-content bg-white p-5">
                                <div class="blog-item-meta bg-gray py-1 px-2">
                                    <span class="text-muted text-capitalize mr-3"><i class="ti-comment mr-2"></i><span class="counter">${post.comments_count}</span> Comments</span>
                                    <span class="text-muted text-capitalize mr-3"><i class="ti-thumb-up mr-2"></i><span class="counter">${post.likes_count}</span> Likes</span>
                                    <span class="text-black-50 text-capitalize mr-3"><i class="ti-eye mr-1">&nbsp;<span class="counter">${post.views}</span></i></span>
                                    <span class="text-danger  text-capitalize mr-3 float-right">
                                        <i style="cursor:pointer" class="ti-trash mr-1" onclick="deleteArticle('${post.id}')"></i>
                                    </span>
                                </div>
                                <h3 class="mt-3 mb-3"><a href="blog-single.html">${post.title}</a></h3>
                                
                                <p class="mb-4">
                                <span class="text-muted text-capitalize mr-3 float-left"><i class="ti-timer mr-1"> ${new Date(post.created_at).toLocaleDateString()}</i></span>
                                ${post.content}</p>
                                <button class="btn btn-small btn-warning btn-round-full" onclick="editArticle('${post.id}')">編輯</button>
                            </div>
                        </div>
                    </div>
                `;
                articlesContainer.insertAdjacentHTML('beforeend', articleHTML);
            });
            currentPage = page;
            totalPages = data.total_pages;
            document.getElementById('current-page').textContent = currentPage;
            updatePagination();
            // 初始化 counterup
            $('.counter').counterUp({
                delay: 10,
                time: 1000
            });
        })
        .catch(error => console.error('Error fetching articles:', error));
}

function updatePagination() {
    const paginationContainer = document.getElementById('pagination-container');
    paginationContainer.innerHTML = '';

    if (currentPage > 1) {
        paginationContainer.innerHTML += `<a class="prev page-numbers" href="#" onclick="fetchArticles(${currentPage - 1})"><i class="ti-arrow-left mr-2"></i></a>`;
    }

    for (let i = 1; i <= totalPages; i++) {
        paginationContainer.innerHTML += `<a class="page-numbers ${i === currentPage ? 'current' : ''}" href="#" onclick="fetchArticles(${i})">${i}</a>`;
    }

    if (currentPage < totalPages) {
        paginationContainer.innerHTML += `<a class="next page-numbers" href="#" onclick="fetchArticles(${currentPage + 1})"><i class="ti-arrow-right mr-2"></i></a>`;
    }
}

function editArticle(id) {
    window.location.href = `/accounts/edit-article/${id}/`;
}

function deleteArticle(id) {
    Swal.fire({
        title: '確定要刪除這篇文章嗎？',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: '是的，刪除它！',
        cancelButtonText: '取消'
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/api/post/${id}/delete/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (response.status === 204) {
                    Swal.fire(
                        '刪除成功！',
                        '文章已被刪除。',
                        'success'
                    );
                    fetchArticles(currentPage);
                } else {
                    Swal.fire(
                        '刪除失敗',
                        '無法刪除文章。',
                        'error'
                    );
                }
            })
            .catch(error => {
                console.error('Error deleting article:', error);
                Swal.fire(
                    '刪除失敗',
                    '無法刪除文章。',
                    'error'
                );
            });
        }
    });
}

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

document.addEventListener('DOMContentLoaded', () => {
    fetchArticles(currentPage);
    // 每 60 秒更新一次文章數據
    setInterval(() => {
        fetchArticles(currentPage);
    }, 60000); // 60000 毫秒 = 60 秒
});