from datetime import date
from dataclasses import dataclass

from tiny_web.api import Api

from middlewares import MethodOverrideMiddleware


app = Api()
app.add_middleware(MethodOverrideMiddleware)


# Model
@dataclass
class Post:
    id: int
    title: str
    body: str
    author: str
    created_at: date


# Toy ORM
class PostBase:
    _id = 0

    def __init__(self):
        self._posts = []

    def all(self):
        return [post.__dict__ for post in self._posts]

    def get(self, id: int):
        for post in self._posts:
            if post.id == id:
                return post.__dict__
        return None

    def create(self, **kwargs):
        self._id += 1
        kwargs['id'] = self._id
        kwargs['created_at'] = date.today().isoformat()
        new_post = Post(**kwargs)
        self._posts.append(new_post)
        return new_post.__dict__

    def save(self, id: int, **kwargs: dict):
        for post in self._posts:
            if post.id == id:
                for attr, value in kwargs.items():
                    if attr == '_method':
                        continue
                    setattr(post, attr, value)

    def delete(self, id: int):
        for idx, post in enumerate(self._posts):
            if post.id == id:
                del self._posts[idx]


# Init db
db = PostBase()


# Helper
def check_id(func):
    def wrapper(*args, **kwargs):
        id: str = kwargs['id']
        if not id.isnumeric():
            app.not_found(args[-2])
        return func(*args, **kwargs)
    return wrapper


# Routes
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


@app.route('/posts/new')
class NewPostView:
    def get(self, request, response):
        response.html = app.template('blog/post_form.html')
        return response


@app.route('/posts/edit/{id}')
class EditPostView:
    @check_id
    def get(self, request, response, id: str):
        post = db.get(int(id))
        response.html = app.template('blog/post_form.html', {'post': post})
        return response


@app.route('/posts')
class PostsListView:
    def get(self, request, response):
        posts_list = db.all()
        response.json = {'posts': posts_list}
        return response

    def post(self, request, response):
        values = [val for val in request.POST.values() if val]
        if not values:
            message = 'Please fill the form'
            response.html = app.template('blog/post_form.html',
                                         {'message': message})
            return response
        db.create(**request.POST)
        response.html = app.template('blog/post_list.html')
        return response


@app.route('/posts/{id}')
class PostDetailView:
    def get(self, request, response, id: str):
        if not id.isnumeric():
            return app.not_found(response)
        post = db.get(int(id))
        if post is None:
            return app.not_found(response)
        response.html = app.template('blog/post_detail.html', {'post': post})
        return response

    def put(self, request, response, id: str):
        if not id.isnumeric():
            return app.not_found(response)
        db.save(int(id), **request.POST)
        response.html = app.template('blog/post_list.html')
        return response

    def delete(self, request, response, id: str):
        if not id.isnumeric():
            return app.not_found(response)
        db.delete(int(id))
        response.html = app.template('blog/post_list.html')
        return response
