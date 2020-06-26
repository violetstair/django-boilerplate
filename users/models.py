import re
import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models, transaction

GENDER_CHOICE = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
    ('None', 'None'),
)


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, username, password=None):
        # email 검증
        if not email or email != self.normalize_email(email):
            raise ValueError('failed email validate check')

        # username 검증
        if re.findall(r'([A-Z|a-z|\d]+)', username)[0] != username:
            raise ValueError('failed username validate check')

        # password 검증
        if not re.match(r'(?=[^A-Z]*[A-Z])(?=[^a-z]*[a-z])(?=[^0-9]*[0-9])', password):
            raise ValueError('failed password validate check')

        user = self.model(
            email=email,
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=email,
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, models.Model):
    objects = UserManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=256, null=False, unique=True, verbose_name='이메일')
    username = models.CharField(max_length=20, null=False, unique=True, verbose_name='사용자이름')
    is_active = models.BooleanField(default=True, verbose_name='활성 계정')
    is_admin = models.BooleanField(default=False, verbose_name='관리자')
    is_superuser = models.BooleanField(default=False, verbose_name='최상위 관리자')
    is_staff = models.BooleanField(default=False, verbose_name='운영자')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='가입일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='최근접속')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    def __str__(self):
        return f'{self.username}:{self.email}'

    class Meta:
        db_table = 'accounts'
        verbose_name = '회원정보'
        verbose_name_plural = '회원목록'
        ordering = ['-created_at']

    @staticmethod
    def get_user(user_id):
        return User.objects.filter(
            id=user_id,
            is_admin=False,
            is_superuser=False,
            is_staff=False,
        )


class Profile(models.Model):
    user = models.OneToOneField(
        to='User',
        on_delete=models.DO_NOTHING,
        primary_key=True,
        related_name='user_profile',
        verbose_name='사용자'
    )
    nickname = models.CharField(max_length=64, null=False, verbose_name='별명')
    bio = models.TextField(max_length=512, null=True, blank=True, verbose_name='자기소개')
    address = models.CharField(max_length=256, null=True, blank=True, verbose_name='주소')
    birthday = models.DateField(null=True, verbose_name='생일')
    gender = models.CharField(max_length=20, verbose_name='성별', choices=GENDER_CHOICE, default='None')
    phone = models.CharField(max_length=13, null=True, blank=True, verbose_name='전화번호')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='추가일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='마지막 수정')

    def __str__(self):
        return f'{self.user.username}:{self.nickname}'

    class Meta:
        db_table = 'profiles'
        verbose_name = '프로필'
        verbose_name_plural = '프로필목록'
        ordering = ['user']

    @staticmethod
    def create_profile(data):
        profile = Profile(
            user=data['user'],
            nickname=data['nickname'],
            bio=data['bio'],
            address=data['address'],
            birthday=data['birthday'],
            gender=data['gender'],
            phone=data['phone'],
        )
        profile.save()
        return profile

    @staticmethod
    def update_profile(instance, data):
        profile = Profile.objects.get(user=data['user'])

        if instance.nickname != data['nickname']:
            profile.nickname=data['nickname']

        if instance.bio != data['bio']:
            profile.bio = data['bio']

        if instance.address != data['address']:
            profile.address = data['address']

        if instance.birthday != data['birthday']:
            profile.birthday = data['birthday']

        if instance.gender != data['gender']:
            profile.gender = data['gender']

        if instance.phone != data['phone']:
            profile.phone = data['phone']

        profile.save()
        return profile

    @staticmethod
    def get_profile(user_id):
        profile = Profile.objects.filter(
            user=user_id,
        ).first()
        return profile
