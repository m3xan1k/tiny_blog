

window.addEventListener('DOMContentLoaded', () => {
    const div = document.querySelector('#blog');
    const url = '/posts'

    fetch(url)
        .then((resp) => resp.json())
        .then((data) => {
            let content = '';
            if (data.posts.length == 0) {
                content += 'No posts yet...';
            }
            data.posts.forEach(post => {
                let post_content = `<div class="card col-4 mx-auto mb-5 p-5">
                    <h2>${post.title}</h2>
                    <h5>${post.author}</h5>
                    <h6>${post.created_at}</h6>
                    <a href="/posts/${post.id}" class="btn btn-secondary">Read more</a>
                </div>`;
                content += post_content;
            });
            div.innerHTML = content;
        })
})
