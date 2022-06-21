from django.db import models
from users.models import User
from PIL import Image as Img
from django.core.validators import MinLengthValidator
from .validators import FileValidator
from django.urls import reverse


def upload_to(instance, filename):
    return f"images/{filename}"


class Image(models.Model):
    name = models.CharField(
        validators=[
            MinLengthValidator(2, "The field must contain at least 2 characters")
        ],
        max_length=255,
        blank=True,
        null=True,
        unique=True,
    )
    image = models.ImageField(
        upload_to=upload_to,
        validators=[
            FileValidator(
                max_size=1920 * 1080, content_types=("image/jpeg", "image/png")
            )
        ]
    )
    original_image_link = models.CharField(max_length=2500, default="", blank=True, null=True)
    thumbnails_links = models.JSONField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return f'{self.id}, {self.owner}: "{self.name}"'

    def update_thumbnails(self, thumbnails_sizes):
        if thumbnails_sizes is None:
            thumbnails_sizes = []

        if self.thumbnails_links is None:
            self.thumbnails_links = {}

        unique_thumbnails_sizes = set(map(str, thumbnails_sizes))
        if set(self.thumbnails_links.keys()) == unique_thumbnails_sizes:
            return

        new_thumbnails_links = {
            size: self.thumbnails_links.get(size, "")
            for size in unique_thumbnails_sizes
        }

        self.thumbnails_links = new_thumbnails_links
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        thumbnail_sizes = self.owner.user_tier.thumbnails_sizes["sizes"]
        if not self.thumbnails_links:
            self.thumbnails_links = {}
        for size in thumbnail_sizes:
            self.thumbnails_links[size] = reverse("get_or_create_thumbnail_link", args=[self.owner, size, self.name])

        print("\n\nself.thumbnails_links:", self.thumbnails_links)

        super().save(*args, **kwargs)
        # przeiteruj wszystkie thumbnail sizes swojego tieru
        # i je wygeneruj

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Img.open(self.image.url.lstrip('/'))
    #     width, height = img.size
    #     """for new_height in user's_user_tier_allowed_sizes:
    #         img.thumbnail((calculated sizes))
    #         img.save(f'media/images/{self.owner}_{self.name}_{new_height}.jpg')
    #     """
    #     new_height = 100
    #     img.thumbnail((new_height, int(width * (new_height / height))))
    #     img.save(f'media/images/{self.owner}_{self.name}_{new_height}.png')
