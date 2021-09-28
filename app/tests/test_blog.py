import unittest
from app import Blog
from app import User

class PitchModelTest(unittest.TestCase):
    def setUp(self):
        self.user_Hope = User(username='shereny', password='reny', email='test@test.com')
        self.new_blog = Blog (id=1, title='Test', content=' test your blog', user_id=self.user_Hope.id)

    def tearDown(self):
        Blog.query.delete()
        User.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_blog.title, 'Test')
        self.assertEquals(self.new_blog.content, 'test your blog')
        self.assertEquals(self.new_blog.user_id, self.user_Hope.id)

    def test_save_pitch(self):
        self.new_blog.save()
        self.assertTrue(len(Blog.query.all()) > 0)

    def test_get_blog(self):
        self.new_blog.save()
        got_pitch = Blog.get_blog(1)
        self.assertTrue(Blog.get_blog is not None)