from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        # if not email:
        #     raise ValueError('The given email must be set')
        email = self.normalize_email(email)

        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
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


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    display_name = models.CharField(_('name'), max_length=30)
    email = models.EmailField(_('email address'), unique=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    icon = models.ImageField(upload_to='account', blank=True)

    GENDER_CHOICES = (
        ('女性', '女性',),
        ('男性', '男性',),
        ('秘密', '秘密',)
    )
    gender = models.CharField(
        max_length=50, blank=True, choices=GENDER_CHOICES
    )

    def make_select_object(from_x, to_y, dates, increment=True):
        if increment:
            for i in range(from_x, to_y):
                dates.append([i, i])
            else:
                for i in range(from_x, to_y, -1):
                    dates.append([i, i])
        return dates

    years = []
    current_year = datetime.now().year
    BIRTH_YEAR_CHOICES = make_select_object(
        current_year+1, current_year-80, years
    )
    for i in range(len(BIRTH_YEAR_CHOICES)):
        BIRTH_YEAR_CHOICES[i] = [str(j) for j in BIRTH_YEAR_CHOICES[i]]
    birth_year = models.CharField(
        max_length=20, blank=True, choices=BIRTH_YEAR_CHOICES
    )

    months = []
    BIRTH_MONTH_CHOICES = make_select_object(1, 13, months)
    for i in range(len(BIRTH_MONTH_CHOICES)):
        BIRTH_MONTH_CHOICES[i] = [str(j) for j in BIRTH_MONTH_CHOICES[i]]
    birth_month = models.CharField(
        max_length=20, blank=True, choices=BIRTH_MONTH_CHOICES
    )

    LOCATION_CHOICES = (
        ('北海道', '北海道',),
        ('東北', '東北',),
        ('関東', '関東',),
        ('中部', '中部',),
        ('近畿', '近畿',),
        ('中国', '中国',),
        ('四国', '四国',),
        ('九州', '九州',)
    )
    location = models.CharField(
        max_length=50, blank=True, choices=LOCATION_CHOICES
    )
    favorite_word = models.CharField(max_length=50, blank=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_name(self):
        return self.display_name

    def __str__(self):
        return self.username
