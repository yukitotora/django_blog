from django.db import models
from django.utils import timezone
from django.urls import reverse

from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import EmailValidator

# Userモデルのマネジャー
class CustomUserManager(UserManager):

    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        elif not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username = username,
            email = self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, email, password, **extra_fields)

# Userモデルのクラス
class User(AbstractBaseUser, PermissionsMixin):

    # Userモデルの基本項目
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    # adminサイトへのアクセス権をユーザーが持っているか判断するメソッド
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether this user can log into this admin site.'),
    )

    # ユーザーがアクティブかどうか判断するメソッド
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active.'
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    # ユーザー名として使うフィールド、スーパーユーザーを作る際に必ず入力するべきフィールドを指定している
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class Post(models.Model):
    #ブログのポストモデル
    title = models.CharField('タイトル', max_length=100)
    author = models.ForeignKey('Author', on_delete=models.PROTECT, verbose_name='投稿者')
    post_date = models.DateTimeField('投稿日時', default=timezone.now)
    content = models.TextField('本文', max_length=1000, help_text='1000文字以内で本文を入力してください')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='カテゴリ')
    tag = models.ManyToManyField('Tag', blank=True, help_text='タグを選んでください', verbose_name='タグ')
    # post_dateでソートする
    class Meta:
        ordering = ['-post_date']
    # 詳細ページに飛べるようにする
    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])
    def __str__(self):
        # 管理サイトなどでの表示
        return self.title


class Author(models.Model):
    # ブロガーのモデル
    name = models.CharField('名前', max_length=100)
    bio = models.TextField('自己紹介', max_length=1000)
    # 詳細ページに飛べるようにする
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        # 管理サイトなどでの表示名
        return self.name


class Comment(models.Model):
    # コメントのモデル
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='投稿者', null=True, blank=True)
    text = models.TextField('コメント', max_length=500, help_text='500文字以内でコメントをどうぞ')
    target = models.ForeignKey('Post', on_delete=models.PROTECT, verbose_name='どの記事へのコメントか')
    post_date = models.DateTimeField('投稿日時', default=timezone.now)

    def __str__(self):
        # 管理サイトなどでの表示
        return self.text

    # post_dateでソートする
    class Meta:
        ordering = ['-post_date']


class Category(models.Model):
    # カテゴリのモデル
    name = models.CharField('カテゴリ名', max_length=200, unique=True)

    def __str__(self):
        # 管理サイトなどでの表示名
        return self.name


class Tag(models.Model):
    # タグのモデル
    name = models.CharField('タグ名', max_length=200, unique=True)

    def __str__(self):
        # 管理サイトなどでの表示名
        return self.name
