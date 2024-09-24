from django.contrib.auth.models import AbstractUser
from django.core.validators import (FileExtensionValidator, MaxValueValidator,
                                    MinValueValidator)
from django.db.models import (CASCADE, CharField, FileField, ImageField,
                              IntegerField, ManyToManyField, Model,
                              OneToOneField, SlugField, TextChoices)
from django.utils.text import slugify


class RoleChoice(TextChoices):
    ADMIN = "admin", "Admin"
    USER = "user", "User"


class Account(AbstractUser):
    phone = CharField(max_length=128, unique=True)
    avatar = ImageField(upload_to="avatars/", default="avatar1.jpg")
    music = FileField(
        upload_to="user-files/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["mp3", "ogg"])],
    )
    rating = IntegerField(
        validators=(MaxValueValidator(5), MinValueValidator(1)), default=-1
    )
    role = CharField(max_length=5, choices=RoleChoice.choices, default=RoleChoice.USER)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class AccountProfile(Model):
    account = OneToOneField(Account, CASCADE, related_name="profile")
    city = CharField(max_length=128, null=True)
    passport_number = CharField(max_length=6, null=True, blank=True)
    passport_letter = CharField(max_length=2, null=True, blank=True)
    interests = ManyToManyField("Interest", "accounts")

    #
    # class Meta:
    #     unique_together = ('passport_number', 'passport_letter')


class Interest(Model):
    name = CharField(max_length=128)
    slug = SlugField(unique=True, blank=True)

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(
            *args,
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )
