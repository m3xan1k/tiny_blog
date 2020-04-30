from datetime import date
from typing import NamedTuple

from tiny_web.api import Api


app = Api()


class Post(NamedTuple):
    id: int
    title: str
    body: str
    author: str
    created_at: date


class PostBase:
    _id = 0

    def __init__(self):
        self._posts = []

    def all(self):
        return [post._asdict() for post in self._posts]

    def get(self, id: int):
        for post in self._posts:
            if post.id == id:
                return post._asdict()
        return None

    def create(self, **kwargs):
        self._id += 1
        kwargs['id'] = self._id
        kwargs['created_at'] = date.today().isoformat()
        new_post = Post(**kwargs)
        self._posts.append(new_post)
        return new_post._asdict()

    def delete(self, id):
        for idx, post in enumerate(self._posts):
            if post.id == id:
                del self._posts[idx]


db = PostBase()


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
    posts_list = db.all()
    response.json = {'posts': posts_list}
    return response


@app.route('/posts/new')
class PostNewController:
    def get(self, request, response):
        response.html = app.template('blog/post_new.html')
        return response

    def post(self, request, response):
        db.create(**request.POST)
        response.html = app.template('blog/post_list.html')
        return response


@app.route('/posts/delete/{id}')
def delete(request, response, id: str):
    if not id.isnumeric():
        return app.not_found(response)
    db.delete(int(id))
    response.html = app.template('blog/post_list.html')
    return response


@app.route('/posts/{id}')
def get_detail(request, response, id: str):
    if not id.isnumeric():
        return app.not_found(response)
    post = db.get(int(id))
    if post is None:
        return app.not_found(response)
    response.html = app.template('blog/post_detail.html', {'post': post})
    return response
