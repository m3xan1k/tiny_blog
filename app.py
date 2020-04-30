from datetime import date

from tiny_web.api import Api


app = Api()

posts_list = [
    {
        'id': 1,
        'title': 'Very first post',
        'body': 'Hello everyone who visit first post',
        'author': 'm3xan1k',
        'created_at': date.today().isoformat()
    },
    {
        'id': 2,
        'title': 'Second post',
        'body': 'Hello everyone who visit second post',
        'author': 'm3xan1k',
        'created_at': date.today().isoformat()
    },
    {
        'id': 3,
        'title': 'Third post',
        'body': 'Hello everyone who visit third post',
        'author': 'm3xan1k',
        'created_at': date.today().isoformat()
    },
]


@app.route('/')
def index(request, response):
    response.html = app.template('index.html')
    return response


@app.route('/about')
def about(request, response):
    response.html = app.template('about.html')
    return response


@app.route('/blog')
def blog(request, response):
    response.html = app.template('blog/post_list.html')
    return response


@app.route('/posts')
def posts(request, response):
    response.json = {'posts': posts_list}
    # response.json = {'hello': 'world'}
    return response


@app.route('/posts/{id}')
def post(request, response, id: str):
    if not id.isnumeric():
        app.not_found(response)
    post = [post for post in posts_list if post['id'] == int(id)][0]
    response.html = app.template('blog/post_detail.html', {'post': post})
    return response
