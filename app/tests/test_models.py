import unittest
from flask import current_app
from blog import create_app, db
from accounts import models as accounts_models
from main import models as main_models


class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        db_name = current_app.config['MONGODB_SETTINGS']['DB']
        db.connection.drop_database(db_name)
        self.app_context.pop()


    def test_db_is_testing(self):
        self.assertTrue(current_app.config['MONGODB_SETTINGS'].get('DB')=='RobotBlogTest')


    def test_create_user(self):
        user = accounts_models.User()

        user.username = 'robotblog'
        user.email = 'robotblog@example.com'
        user.password = 'robotblog_password'
        user.is_superuser = False
        user.role = 'editor'
        user.display_name = 'RobotBlog'
        user.biography = 'robotblog description'
        user.homepage_url = 'http://blog.igevin.info'

        user.save()

        created_user = accounts_models.User.objects.get(username='robotblog')

        self.assertTrue(created_user is not None and created_user.email=='robotblog@example.com')

    def test_create_post(self):
        post = main_models.Post()

        post.title = 'title'
        post.slug = 'slug'
        post.fix_slug = '1'
        post.abstract = 'abstract'
        post.raw = 'content'
        user = accounts_models.User()
        user.username='user'
        user.password='password'
        user.save()
        post.author = user
        post.category = 'category1'
        post.tags = ['tag1']

        post.save()

        post = main_models.Post.objects.get(slug='slug')

        self.assertTrue(post is not None and post.title=='title')
