import re
import uuid
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
    Group,
    Permission
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core import validators
from localflavor.br.models import BRCPFField
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    def create_user(
        self, username, cpf, email, first_name, last_name, password=None
    ):
        if not cpf:
            raise ValueError(_('Users must have an CPF'))

        if not email:
            raise ValueError(_('Users must have an email.'))

        user = self.model(
            username=username,
            cpf=cpf,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username, cpf, email, first_name, last_name, password=None
    ):
        user = self.create_user(
            username=username,
            email=email,
            cpf=cpf,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        verbose_name=_('Username'),
        max_length=150,
        unique=True,
        db_index=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ '
            'only.'
        ),
        validators=[username_validator],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    first_name = models.CharField(_("First Name"), max_length=150)
    last_name = models.CharField(_("Last Name"), max_length=150)
    email = models.EmailField(
        verbose_name=_('Email'),
        unique=True,
        db_index=True,
        help_text=_(
            'The email will be used to access the system and send information'
        ),
        validators=[validators.EmailValidator()],
        error_messages={
            'unique': _('This email already exists'),
        },
    )
    cpf = BRCPFField(
        verbose_name="CPF",
        unique=True,
        db_index=True,
    )
    is_staff = models.BooleanField(
        verbose_name=_('Staff Status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_admin = models.BooleanField(
        verbose_name=_('Admin'),
        default=False,
    )
    is_superuser = models.BooleanField(
        verbose_name=_('Super User'),
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name=_('Active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="user_set",
        related_query_name="user",
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'cpf', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('Dealer')
        verbose_name_plural = _('Resellers')
        ordering = ('first_name',)

    def __str__(self):
        return self.email

    def clean(self):
        super(User, self).clean()
        self.email = self.__class__.objects.normalize_email(self.email)
        first_name = self.first_name
        last_name = self.last_name
        self.first_name = first_name.capitalize()
        self.last_name = last_name.capitalize()
        self.cpf = re.sub(r"[\W_]+", "", self.cpf)
