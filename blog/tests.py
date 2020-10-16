from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post

class BlogTests(TestCase):

  def setUp(self):
    self.user =get_user_model().objects.create_user(
      username = 'testuser', 
      email = 'test@email.com', 
      password = 'secret'
    )

    self.post = Post.objects.create(
      title = 'a good title', 
      body = 'a great blog', 
      author = self.user
    )

    def test_model_string(self):
      post = Post(title='a good title')
      self.assertEqual(str(post), post.title)

    def test_post_content(self):
      self.assertEqual(f'{self.post.title}', 'a good title')
      self.assertEqual(f'{self.post.body}', 'a great blog')
      self.assertEqual(f'{self.post.author}', 'username')

    def test_post_list_view(self):
      response = self.client.get(reverse('home'))
      self.assertEqual(response.status_code, 200)
      self.assertContains(response, 'a great blog')
      self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
      response = self.client.get('/post/1/')
      no_response = self.client.get('/post/100000/')
      self.assertEqual(response.status_code, 200)
      self.assertEqual(no_response.status_code, 404)
      self.assertContains(response, 'a good blog')
      self.assertTemplateUsed(response, 'post_detail.html')

    

