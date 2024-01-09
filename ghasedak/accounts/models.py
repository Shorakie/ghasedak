from django.contrib.auth.models import PermissionsMixin, UserManager as DjangoUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from ghasedak.common.models import UniversalModel, ActivatedModel, TimestampedModel
from ghasedak.common.validators import UsernameValidator, DigitValidator, phone_number_validator


class UserManager(DjangoUserManager):
    use_in_migrations = False

    def _create_user(self, username, *args, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")

        user = self.model(username=username, **extra_fields)
        user.save(using=self._db)
        return user


class User(UniversalModel, TimestampedModel, ActivatedModel, PermissionsMixin):
    username = models.CharField(
        verbose_name=_('username'),
        max_length=16,
        unique=True,
        help_text=_('Required between 3 and 16 characters. Letters, digits and \'_\' only.'),
        validators=[UsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    phone = models.CharField(
        verbose_name=_('phone'),
        max_length=15,
        validators=[
            DigitValidator(),
            phone_number_validator,
        ],
        db_index=True,
        blank=True,
        help_text=_('Valid phone number in E.164 international form.'),
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    last_login = models.DateTimeField(_("last login"), blank=True, null=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone']

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.get_username()

    def get_username(self):
        """Return the username for this User."""
        return getattr(self, self.USERNAME_FIELD)

    def natural_key(self):
        return (self.get_username(),)

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True
