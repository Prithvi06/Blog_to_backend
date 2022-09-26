from xml.parsers.expat import model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=20, default="first")
    middle_name = models.CharField(max_length=20, default="middle")
    last_name = models.CharField(max_length=20, default="last")
    image = models.ImageField(upload_to='image/', blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class BlogPost(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='image/', blank=True)
    text = models.TextField(blank=True)
    published_at = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    likes = models.ManyToManyField(User, blank=True)
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES,
                                                        default ='draft')
    
    
    class Meta:
        ordering = ('-published_at', )
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, related_name="user_comment", on_delete=models.CASCADE)
    blogpost = models.ForeignKey(BlogPost, related_name="comments", on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    body = models.TextField()

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.user.email)


class Reply(models.Model):
    user = models.ForeignKey(User, related_name="user_reply", on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name="replies", on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    body = models.TextField()

    def __str__(self):
        return 'Reply {} on {}'.format(self.body, self.comment)


class BlackListedToken(models.Model):
    token = models.CharField(max_length=500)
    user = models.ForeignKey(User, related_name="token_user", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("token", "user")