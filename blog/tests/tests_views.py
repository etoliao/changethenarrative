from django.test import TestCase
from django.shortcuts import reverse
from blog.models import Post
from django.contrib.auth import get_user_model
from django.utils.timezone import timedelta, now
from .factories import UserFactory, PostFactory

class PostListTest(TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("post_list")
        
    def test_noposts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["posts"]), 0)
    
    def test_showposts(self):
        author = UserFactory()
        yest = now() - timedelta(days=1)
        tom = now() + timedelta(days=1)
        postyest = PostFactory(published_date=yest, text="something")
        posttom = PostFactory(published_date=tom, text= "nothing")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["posts"]), [postyest])
        self.assertIn("something", response.content.decode("utf-8"))
        self.assertNotIn("nothing", response.content.decode("utf-8"))

class PostDetailTest(TestCase):
    def setUp(self):
        super().setUp()
        self.author = UserFactory(username="test user", password="testpassword")
        self.tom = now() + timedelta(days=1)
        self.yest = now() - timedelta(days=1)

    def test_postnonexistant(self):
        url = reverse("post_detail", kwargs= {"pk": 1000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_postexistant_notloggedin(self):
        postyest = PostFactory(published_date=self.yest, text="something")
        url = reverse("post_detail", kwargs= {"pk": postyest.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_postexistant_loggedin(self):
        self.assertTrue(self.client.login(username="test user", password="testpassword"))
        postyest = PostFactory(published_date=self.yest, text="something")
        url = reverse("post_detail", kwargs= {"pk": postyest.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_notpublishedpost_notloggedin(self):
        """identifies a non-published post and returns an error if not logged in"""
        self.client.logout()
        posttom = PostFactory(published_date=self.tom, text= "nothing")
        url = reverse("post_detail", kwargs= {"pk": posttom.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_notpublishedpost_loggedin(self):
        """identifies a non-published post and allows a logged in user"""
        posttom = PostFactory(published_date=self.tom, text= "nothing")
        url = reverse("post_detail", kwargs= {"pk": posttom.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

class PostNewTest(TestCase):
    def setUp(self):
        super().setUp()
        self.author = UserFactory(username="test user", password="testpassword")
        self.url = reverse("post_new")
        self.postdata = {
            "title": "testpost",
            "text": "testtext",
        }

    def test_nonewpostspage_notloggedin(self):
        """if a user is not logged in, they cannot access the new posts page"""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_newpostspage_loggedin(self):
        """if a user is logged in, they can access new posts page"""
        self.assertTrue(self.client.login(username="test user", password="testpassword"))
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_createpost_notloggedin(self):
        """if user is not logged in, cannot create post"""
        self.client.logout()
        response = self.client.post(self.url, self.postdata)
        self.assertEqual(response.status_code, 404)

    def test_createpost_loggedin(self):
        """if user is logged in, can create post"""
        self.assertTrue(self.client.login(username="test user", password="testpassword"))
        response = self.client.post(self.url, self.postdata)
        newpost = Post.objects.get(title=self.postdata["title"], text=self.postdata["text"])
        expectedurl = reverse("post_detail", kwargs={"pk": newpost.pk})
        self.assertRedirects(response, expectedurl)

class PostEditTest(TestCase):
    def setUp(self):
        super().setUp()
        self.author = UserFactory(username="test user", password="testpassword")
        self.postdata = {
            "title": "testpost",
            "text": "testtext",
        }
        self.yest = now() - timedelta(days=1)
        self.tom = now() + timedelta(days=1)

    def test_editingposts_notloggedin(self):
        """if a user is not logged in, they cannot access the edit posts page"""
        self.client.logout()
        response = self.client.post(self.postdata) 
        self.assertEquals(response.status_code, 404)

    def test_editingposts_loggedin(self):
        """if user is logged in, can edit post"""
        self.assertTrue(self.client.login(username="test user", password="testpassword"))
        post = PostFactory(text="something")
        url = reverse("post_edit", kwargs= {"pk": post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_editpubposts_notloggedin(self):
        """if logged out, cannot edit published posts"""
        self.client.logout()
        postyest = PostFactory(published_date=self.yest, text="something")
        url = reverse("post_edit", kwargs= {"pk": postyest.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_editpubposts_loggedin(self):
        """if logged in, can edit published posts"""
        self.assertTrue(self.client.login(username="test user", password="testpassword"))
        postyest = PostFactory(published_date=self.yest, text="something")
        url = reverse("post_edit", kwargs= {"pk": postyest.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_editnonpubposts_notloggedin(self):
        """if a user is not logged in, they cannot edit unpublished posts"""
        self.client.logout()
        posttom = PostFactory(published_date=self.tom, text= "nothing")
        url = reverse("post_edit", kwargs= {"pk": posttom.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_editnonpubposts_loggedin(self):
        """if a user is logged in, they can edit unpublished posts"""
        self.assertTrue(self.client.login(username="test user", password="testpassword"))
        posttom = PostFactory(published_date=self.tom, text= "nothing")
        url = reverse("post_edit", kwargs= {"pk": posttom.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_editnonexistantpost_loggedin(self):
        """a logged in user cannot edit a post that doesn't exist"""
        self.assertTrue(self.client.login(username="test user", password="testpassword"))
        url = reverse("post_detail", kwargs= {"pk": 1000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_editinvalidpost_loggedin(self):
        """a logged in user cannot edit a post that is invalid"""
        self.assertTrue(self.client.login(username="test user", password="testpassword"))
        response = self.client.post(self.postdata) 
        self.assertEquals(response.status_code, 404)
