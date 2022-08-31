""" Call functions to deliver web pages and other content """
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit  import CreateView, UpdateView
from django.http import JsonResponse

import requests

from .models import Post, Comment
from .forms import CommentForm


URL = "http://127.0.0.1:9821/"

def api_json_format(path):
    """Convert the type of api data into json format

    Args:
        path: URL path

    Returns:
        Json:
    """
    return requests.get(f'{URL}{path}').json()

def api_data(request):
    """Feed(Populate) blog database with Users, Posts, and Comments API

    Args:
        request (Http Request)

    Returns:
        Json: successful message
    """
    # All users
    users_api = api_json_format('users')
    user_dict ={ }
    for user in users_api:
        if not user['mail'] or not user['password']:
            continue
        new_user, created = User.objects.get_or_create(
            username = user['username'],
            email = user['mail'],
            )
        if created:
            new_user.set_password(user['password'])

        user_dict[user['_id']] = new_user

    # All posts
    posts_api = api_json_format('posts')
    for post in posts_api:
        # Get user object (The author of that post)
        author_api = user_dict[post['author']]

        # Check origin value to detect if post doesn't exist, create new one
        new_post, created = Post.objects.get_or_create(
            author = author_api,
            origin = post['_id'],
            )

        if created:
            new_post.created = post['created']
            new_post.updated = post['updated']
            new_post.title = post['title']
            new_post.slug = post['slug']
            new_post.body = post['body']
            new_post.published_at = post['publish']
            new_post.status = post['status']
            # Save changes(Linking objects) to the database
            new_post.save()

    #All comments
    comments_api = api_json_format('comments')
    for comment in comments_api:
        try:
            print(comment['body'])
            # If comment already
            linked_post = Post.objects.get(origin=comment['post_id'])
            new_comment, created = Comment.objects.get_or_create(
                post = linked_post,
                origin = comment['_id'],
                email = comment['email'],
                )
            print(created)
            if created:
                # Link new comment with the post
                print('inside created')
                # time.sleep(32)
                new_comment.name = comment['name']
                new_comment.body = comment['body']
                new_comment.updated_at = comment['updated']
                new_comment.active = comment['active']
                new_comment.created_at = comment['created']
                # Save changes(Linking objects) to the database
                new_comment.save(wait=False)
            print(vars(new_comment))
        except Post.DoesNotExist:
            print("Post doesn't exist")

        except ValueError:
            print("modifying Comment is not allowed in 30s")

    return JsonResponse({'msg': 'Successfully synced'})

def list_all(request):
    """Return all published posts

    Args:
        request (Http Request)

    Returns:
        All published posts
    """
    all_list = Post.published_objects.filter(published_at__lte=timezone.now())
    paginator = Paginator(all_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'post/list_all.html', {
        'page_obj': page_obj,
        })

def detail(request, slug):
    """Render details and comments of a specific Post

    Args:
        request (Http Request)
        slug (Slug)

    Returns:
        HTML : Html file represent the rendered post/comments
    """
    post = get_object_or_404(Post, slug=slug)
    active_comments = Comment.active_objects.filter(post=post)
    if request.method == 'POST':
        # Create a form instance with POST data.
        form = CommentForm(request.POST)

        if form.is_valid():
            # Temporarily create an object to be add some logic into the data
            # if there is such a need before saving into the database
            new_comment = form.save(commit=False)
            # Assign(Link) the comment instance(object) to the current post
            new_comment.post = post

            # Save the new instance into the database
            try:
                new_comment.save()
                return HttpResponseRedirect(reverse('blog:detail', args=(post.slug,)))
            except ValueError:
                form.add_error('body', 'you need to wait for 30s.')

    else:
        # If the request is a GET request then, create an empty
        # form object and render it into the page
        form = CommentForm()

    return render(request, 'post/detail.html', {'post': post,
                'form': form, 'active_comments': active_comments})


class BlogCreateView(LoginRequiredMixin, CreateView):
    """ Create new post only for registered users """
    model = Post
    template_name = "post/add_new.html"
    fields = ('title', 'body', 'status', )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """ Update new post only for the same registered author """
    model = Post
    template_name ='post/edit.html'
    fields = ['title', 'body']

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
