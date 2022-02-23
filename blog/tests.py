from django.test import TestCase
from django.shortcuts import reverse
from blog.models import Post
from django.contrib.auth import get_user_model
from django.utils.timezone import timedelta, now

class PostListTest(TestCase):
    def test_noposts(self):
        url = reverse("post_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["posts"]), 0)
    
    def test_showposts(self):
        User = get_user_model()
        author = User.objects.create(username="test user")
        author.save()
        yest = now() - timedelta(days=1)
        tom = now() + timedelta(days=1)
        postyest = Post.objects.create(title="Yest Post", author=author, published_date=yest, text="something")
        posttom = Post.objects.create(title="Tom Post", author=author, published_date=tom, text= "nothing")
        url = reverse("post_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["posts"]), [postyest])
        self.assertIn("something", response.content.decode("utf-8"))
        self.assertNotIn("nothing", response.content.decode("utf-8"))

class PostDetailTest(TestCase):
    def test_postnonexistant(self):
        url = reverse("post_detail", kwargs= {"pk": 1000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_postexistant_notloggedin(self):
        User = get_user_model()
        author = User.objects.create(username="test user")
        author.save()
        yest = now() - timedelta(days=1)
        postyest = Post.objects.create(title="Yest Post", author=author, published_date=yest, text="something")
        url = reverse("post_detail", kwargs= {"pk": postyest.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_postexistant_loggedin(self):
        User = get_user_model()
        author = User.objects.create(username="test user")
        author.set_password("testpassword")
        author.save()
        self.assertTrue(self.client.login(username="test user", password="testpassword"))
        yest = now() - timedelta(days=1)
        postyest = Post.objects.create(title="Yest Post", author=author, published_date=yest, text="something")
        url = reverse("post_detail", kwargs= {"pk": postyest.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_notpublishedpost_notloggedin(self):
        """identifies a non-published post and returns an error if not logged in"""
        self.client.logout()
        User = get_user_model()
        author = User.objects.create(username="test user")
        author.save()
        tom = now() + timedelta(days=1)
        posttom = Post.objects.create(title="Tom Post", author=author, published_date=tom, text= "nothing")
        url = reverse("post_detail", kwargs= {"pk": posttom.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_notpublishedpost_loggedin(self):
        """identifies a non-published post and allows a logged in user"""
        User = get_user_model()
        author = User.objects.create(username="test user")
        author.save()
        tom = now() + timedelta(days=1)
        posttom = Post.objects.create(title="Tom Post", author=author, published_date=tom, text= "nothing")
        url = reverse("post_detail", kwargs= {"pk": posttom.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

class PostNewTest(TestCase):
    def test_nonewpostspage_notloggedin(self):
        """if a user is not logged in, they cannot access the new posts page"""
        self.client.logout()
        url = reverse("post_new")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_newpostspage_loggedin(self):
        """if a user is logged in, they can access new posts page"""
        User = get_user_model()
        author = User.objects.create(username="test user")
        author.set_password("testpassword")
        author.save()
        self.assertTrue(self.client.login(username="test user", password="testpassword"))
        url = reverse("post_new")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_createpost_notloggedin(self):
        """if user is not logged in, cannot create post"""
        self.client.logout()
        post_data = {
            "title": "testpost",
            "text": "testtext",
        }
        url = reverse("post_new")
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 404)

    def test_createpost_loggedin(self):
        """if user is logged in, can create post"""
        User = get_user_model()
        author = User.objects.create(username="test user")
        author.set_password("testpassword")
        author.save()
        self.assertTrue(self.client.login(username="test user", password="testpassword"))
        postdata = {
            "title": "testpost",
            "text": "testtext",
        }
        url = reverse("post_new")
        response = self.client.post(url, postdata)
        newpost = Post.objects.get(title=postdata["title"], text=postdata["text"])
        expectedurl = reverse("post_detail", kwargs={"pk": newpost.pk})
        self.assertRedirects(response, expectedurl)

class PostEditTest(TestCase):
    def test_editingposts_notloggedin(self):
        """if a user is not logged in, they cannot access the edit posts page"""
        self.client.logout()
        postdata = {
            "title": "testpost",
            "text": "testtext",
        }
        response = self.client.post(postdata) 
        self.assertEquals(response.status_code, 404)

    def test_editingposts_loggedin(self):
        """if user is logged in, can edit post"""
        User = get_user_model()
        author = User.objects.create(username="test user")
        author.set_password("testpassword")
        author.save()
        self.assertTrue(self.client.login(username="test user", password="testpassword"))
        post = Post.objects.create(title="Post", author=author, text="something")
        url = reverse("post_edit", kwargs= {"pk": post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_editpubposts_notloggedin(self):
        """if logged out, cannot edit published posts"""
        self.client.logout()
        User = get_user_model()
        author = User.objects.create(username="test user")
        author.save()
        yest = now() - timedelta(days=1)
        postyest = Post.objects.create(title="Yest Post", author=author, published_date=yest, text="something")
        url = reverse("post_edit", kwargs= {"pk": postyest.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_editpubposts_loggedin(self):
        """if logged in, can edit published posts"""
        User = get_user_model()
        author = User.objects.create(username="test user")
        author.set_password("testpassword")
        author.save()
        self.assertTrue(self.client.login(username="test user", password="testpassword"))
        yest = now() - timedelta(days=1)
        postyest = Post.objects.create(title="Yest Post", author=author, published_date=yest, text="something")
        url = reverse("post_edit", kwargs= {"pk": postyest.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_editnonpubposts_notloggedin(self):
        """if a user is not logged in, they cannot edit unpublished posts"""
        self.client.logout()
        User = get_user_model()
        author = User.objects.create(username="test user")
        author.save()
        tom = now() + timedelta(days=1)
        posttom = Post.objects.create(title="Tom Post", author=author, published_date=tom, text= "nothing")
        url = reverse("post_edit", kwargs= {"pk": posttom.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_editnonpubposts_loggedin(self):
        """if a user is logged in, they can edit unpublished posts"""
        User = get_user_model()
        author = User.objects.create(username="test user")
        author.set_password("testpassword")
        author.save()
        self.assertTrue(self.client.login(username="test user", password="testpassword"))
        tom = now() + timedelta(days=1)
        posttom = Post.objects.create(title="Tom Post", author=author, published_date=tom, text= "nothing")
        url = reverse("post_edit", kwargs= {"pk": posttom.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_editnonexistantpost_loggedin(self):
        """a logged in user cannot edit a post that doesn't exist"""
        User = get_user_model()
        author = User.objects.create(username="test user")
        author.set_password("testpassword")
        author.save()
        self.assertTrue(self.client.login(username="test user", password="testpassword"))
        url = reverse("post_detail", kwargs= {"pk": 1000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_editinvalidpost_loggedin(self):
        """a logged in user cannot edit a post that is invalid"""
        User = get_user_model()
        author = User.objects.create(username="test user")
        author.set_password("testpassword")
        author.save()
        self.assertTrue(self.client.login(username="test user", password="testpassword"))
        postdata = {
            "title": "",
            "text": "",
        }
        response = self.client.post(postdata) 
        self.assertEquals(response.status_code, 404)
