from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Meta:
        db_table = "users"

    first_name = CharField(
        _("first name"), max_length=150, blank=True, default="", null=True
    )
    last_name = CharField(
        _("last name"), max_length=150, blank=True, default="", null=True
    )
    email = EmailField(_("email address"), blank=True, default="", null=True)
    date_joined = None
    last_login = None
