
	document.addEventListener('DOMContentLoaded', function() {
        const slug = document.getElementById('slug-container').dataset.slug;
        fetchArticle(slug);
    });

	function fetchArticle(slug) {
		fetch(`/api/post/article/${slug}/`)
			.then(response => response.json())
			.then(data => {
				addArticleContent(data);
				setupLikeButton(data);
				addNextAndPrevArticle(data);
				addComment(data);
				addCommentForm(data);
			})
			.catch(error => console.error('Error fetching article content:', error));
	}

	document.getElementById('comment-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const comment = document.getElementById('comment').value;
		const post = document.getElementById('comment-form').dataset.post;

        fetch('/api/comment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                content: comment,
				post: post
            })
        })
        .then(response => response.json())
        .then(data => {
			if (data.id && data.created_at) {
				Swal.fire({
					icon: 'success',
					title: '資料已成功更新',
					showConfirmButton: false,
					timer: 1500
				});
				const slug = document.getElementById('slug-container').dataset.slug;
				fetchArticle(slug);
				document.getElementById('comment').value = '';
			} else {
				Swal.fire({
					icon: 'error',
					title: '更新失敗',
					html: '<ul>' + Object.values(data).map(function(error) {
						return '<li>' + error + '</li>';
					}).join('') + '</ul>',
				});
			}
        })
        .catch(error => console.error('Error:', error));
	});

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

    function addArticleContent(data){
        const articleContent = `
            <div class="single-blog-item">
                <div class="blog-item-content bg-white p-5">
                    <div class="blog-item-meta bg-gray py-1 px-2">
                        <span class="text-muted text-capitalize mr-3"><i class="ti-pencil-alt mr-2"></i>${data.category}</span>
                        <span class="text-muted text-capitalize mr-3"><i class="ti-comment mr-2"></i>${data.comments_count} Comments</span>
                        <span class="text-black text-capitalize mr-3"><i class="ti-time mr-1"></i> ${new Date(data.created_at).toLocaleDateString('zh-TW', { year: 'numeric', month: 'long', day: 'numeric' })}</span>
                    </div> 

                    <h2 class="mt-3 mb-4"><a href="/articles_list/${data.slug}">${data.title}</a></h2>
                    ${data.studient_id ? `<p class="lead mb-4">學號: ${data.studient_id}</p>` : ''}

                    <p>${data.content}</p>

                    <h3 class="quote"><a href="${data.link}" target="_blank">${data.link}</a></h3>

                    <div class="tag-option mt-5 clearfix">
                        <ul class="float-left list-inline"> 
                            <li>標籤:</li> 
                            ${data.tags.map(tag => `<li class="list-inline-item">${tag}</li>`).join('')}
                        </ul>        

                        <ul class="float-right list-inline">
                            <li>最後更新: ${new Date(data.updated_at).toLocaleDateString('zh-TW', { year: 'numeric', month: 'long', day: 'numeric' })}</li>
                            <li><a id="like-button" href="#" class=""><i style="color:${data.liked ? '#0000E3' : '#D0D0D0'}" class="ti-thumb-up mr-1"></i><span id="like-content" class="${data.liked ? 'liked' : ''}">${data.liked ? ` ${data.likes_count}` : ` ${data.likes_count}`}</span></a></li>
                        </ul>
                    </div>
                </div>
            </div>
        `;
        document.querySelector('.single-blog-item').innerHTML = articleContent;
    }

    function setupLikeButton(data) {
        const likeButton = document.getElementById('like-button');
        likeButton.addEventListener('click', function(event) {
            event.preventDefault();
            fetch(`/api/post/${data.id}/like_post/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(result => {
                document.querySelector('#like-content').textContent = result.liked ? ` ${result.likes_count}` : ` ${result.likes_count}`;
                likeButton.classList.toggle('liked', result.liked);
				document.querySelector('.ti-thumb-up').style.color = result.liked ? '#0000E3' : '	#D0D0D0	';
            })
            .catch(error => console.error('Error liking post:', error));
        });
    }

	function addNextAndPrevArticle(data){
		const content = `
			${data.previous_post ? `
			<a class="post-prev align-items-center" href="/articles_list/${data.previous_post.slug}">
				<div class="posts-prev-item mb-4 mb-lg-0">
					<span class="nav-posts-desc text-color">- 上一篇</span>
					<h6 class="nav-posts-title mt-1">
						${data.previous_post.title}
					</h6>
				</div>
			</a>` : ''}
			<div class="border"></div>
			${data.next_post ? `
			<a class="posts-next" href="/articles_list/${data.next_post.slug}">
				<div class="posts-next-item pt-4 pt-lg-0">
					<span class="nav-posts-desc text-lg-right text-md-right text-color d-block">- 下一篇</span>
					<h6 class="nav-posts-title mt-1">
						${data.next_post.title}
					</h6>
				</div>
			</a>` : ''}
		`
		document.querySelector('.posts-nav').innerHTML = content;
	}

	function addComment(data){
		
		const comment = `
			<h4 class="mb-4">${data.comments_count} 則留言</h4>
			<ul class="comment-tree list-unstyled">
				${data.comments.map(comment => `
				<li class="mb-5">
					<div class="comment-area-box">

						<h5 class="mb-1">${comment.author}</h5>
						<span>${comment.studinet_id}</span>

						<div class="comment-meta mt-4 mt-lg-0 mt-md-0 float-lg-right float-md-right">
							<span class="date-comm">發布於 ${new Date(comment.created_at).toLocaleString('zh-TW', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' })}</span>
						</div>

						<div class="comment-content mt-3">
							<p>${comment.content}</p>
						</div>
					</div>
				</li>
				`).join('')}
			</ul>
		`;
		document.querySelector('.comment-area').innerHTML = comment;
	}

	function addCommentForm(data){
		const dataPost = document.getElementById('comment-form');
		dataPost.dataset.post = data.id;
	}