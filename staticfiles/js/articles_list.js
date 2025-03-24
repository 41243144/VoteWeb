document.addEventListener('DOMContentLoaded', function() {
    const articlesList = document.getElementById('articles-list');
    const latestPosts = document.getElementById('latest-posts');
    const tagsList = document.getElementById('tags-list');
    const searchInput = document.getElementById('search-input');
    const sortSelect = document.getElementById('sort-select');
    const paginationLinks = document.getElementById('pagination-links');

    let currentPage = 1;

    function fetchArticles(params = '') {
        fetch(`/api/post/all_posts/?page=${currentPage}&${params}`)
            .then(response => response.json())
            .then(data => {
                articlesList.innerHTML = '';
                console.log(data);
                data.results.forEach(post => {
                    
                    const postElement = document.createElement('div');
                    postElement.className = 'col-lg-6 col-md-6 mb-5';
                    postElement.innerHTML = `
                        <div class="blog-item">
                            <div class="blog-item-content bg-white p-4">
                                <div class="blog-item-meta py-1 px-2">
                                    <span class="text-muted mr-3"><i class="ti-eye mr-2"></i><span class="counter">${post.views}</span> 次觀看</span>
                                    <span class="text-muted mr-3"><i class="ti-comment mr-2"></i><span class="counter">${post.comments}</span> 則留言</span>
                                    <span class="text-muted mr-3"><i class="ti-thumb-up mr-2"></i><span class="counter">${post.likes}</span> 個讚</span>
                                    ${post.category ? `<span class="text-muted text-capitalize mr-3"><i class="ti-pencil-alt mr-2"></i>${post.category.name}</span>` : ''}
                                </div>
                                <h3 class="mt-3 mb-3"><a href="/articles_list/${post.slug}/">${post.title}</a></h3>
                                <p class="mb-4">${post.content.substring(0, 10)}...</p>
                                <a href="/articles_list/${post.slug}/" class="btn btn-small btn-main btn-round-full">查看文章</a>
                            </div>
                        </div>
                    `;
                    articlesList.appendChild(postElement);
                });

                // 初始化 counterup 動畫
                $('.counter').counterUp({
                    delay: 10,
                    time: 1000
                });

                // 更新分頁鏈接
                paginationLinks.innerHTML = '';
                if (data.previous) {
                    const prevLink = document.createElement('a');
                    prevLink.className = 'prev page-numbers';
                    prevLink.href = '#';
                    prevLink.textContent = '上一頁';
                    prevLink.addEventListener('click', (e) => {
                        e.preventDefault();
                        currentPage--;
                        fetchArticles(params);
                    });
                    paginationLinks.appendChild(prevLink);
                }
                for (let i = 1; i <= data.total_pages; i++) {
                    const pageLink = document.createElement('a');
                    pageLink.className = `page-numbers ${i === currentPage ? 'current' : ''}`;
                    pageLink.href = '#';
                    pageLink.textContent = i;
                    pageLink.addEventListener('click', (e) => {
                        e.preventDefault();
                        currentPage = i;
                        fetchArticles(params);
                    });
                    paginationLinks.appendChild(pageLink);
                }
                if (data.next) {
                    const nextLink = document.createElement('a');
                    nextLink.className = 'next page-numbers';
                    nextLink.href = '#';
                    nextLink.textContent = '下一頁';
                    nextLink.addEventListener('click', (e) => {
                        e.preventDefault();
                        currentPage++;
                        fetchArticles(params);
                    });
                    paginationLinks.appendChild(nextLink);
                }
            })
            .catch(error => {
                console.error('Error fetching articles:', error);
            });
    }

    function fetchLatestPosts() {
        fetch('/api/post/latest/')
            .then(response => response.json())
            .then(data => {
                latestPosts.innerHTML = '';
                data.forEach(post => {
                    const postElement = document.createElement('div');
                    postElement.className = 'media border-bottom py-3';
                    postElement.innerHTML = `
                        <div class="media-body">
                            <h6 class="my-2"><a href="/articles_list/${post.slug}/">${post.title}</a></h6>
                            <span class="text-sm text-muted">${new Date(post.created_at).toLocaleString('zh-TW', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })}</span>
                        </div>
                    `;
                    latestPosts.appendChild(postElement);
                });
            });
    }

    function fetchTags() {
        fetch('/api/tag/')
            .then(response => response.json())
            .then(data => {
                tagsList.innerHTML = '';
                data.results.forEach(tag => {
                    const tagElement = document.createElement('a');
                    tagElement.href = '#';
                    tagElement.textContent = tag.name;
                    tagElement.addEventListener('click', () => {
                        fetchArticles(`tag=${tag.name}`);
                    });
                    tagsList.appendChild(tagElement);
                });
            });
    }

    searchInput.addEventListener('input', () => {
        currentPage = 1; // 重置頁數到第一頁
        const sortBy = sortSelect.value;
        fetchArticles(`search=${searchInput.value}&sort_by=${sortBy}`);
    });
    
    sortSelect.addEventListener('change', () => {
        currentPage = 1; // 重置頁數到第一頁
        const search = searchInput.value;
        fetchArticles(`search=${search}&sort_by=${sortSelect.value}`);
    });

    fetchArticles();
    fetchLatestPosts();
    fetchTags();
});