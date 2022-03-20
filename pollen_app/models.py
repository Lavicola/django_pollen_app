import sys
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from user.models import CustomUser
from PIL import Image


# Create your models here.


class FLOWER(models.TextChoices):
    NO_FLOWER = "0", "no flower ",
    SOON_FLOWERING = "1", "flowering in development",
    FLOWERS = "2", "flower"


class SEX(models.TextChoices):
    MALE = "0", "male ",
    FEMALE = "1", "female",
    UNKOWN = "2", "unkown"


class SHIPPING(models.TextChoices):
    USA = "0", "usa ",
    EU = "1", "eu",
    INTERNATIONAL = "2", "international"


class Nepenthes(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=100)
    description = models.CharField(
        blank=True,
        max_length=400)  # maybe someone wants to point out something interesting about his plant e.g color and so on

    flower = models.CharField(
        max_length=2,
        choices=FLOWER.choices,
        default=FLOWER.NO_FLOWER
    )
    sex = models.CharField(
        max_length=2,
        choices=SEX.choices,
        default=SEX.UNKOWN
    )
    shipping = models.CharField(
        max_length=2,
        choices=SHIPPING.choices,
        default=SHIPPING.INTERNATIONAL
    )

    isHybrid = models.BooleanField(default=False)
    image = models.FileField(upload_to='images')

    def getUsername(self):
        return CustomUser.objects.filter(id=self.owner_id).first()

    def save(self):
        # remove unnecessary word and decide whether it is a hybride or not
        self.name = self.name.lower().replace("nepenthes ", "")
        if len(self.name.split(" x ")) > 1:
            self.isHybrid = True
        else:
            self.isHybrid = False

        output = self.modifyImage(self.image)

        # change the imagefield value to be the newley modifed image value
        self.image = self.modifyImage(self.image)

        super(Nepenthes, self).save()

    def modifyImage(self, image=None):
        fileending = "webp"
        image = image
        if image == None:
            image = self.image
        im = Image.open(self.image)
        output = BytesIO()

        size = 1280, 720
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(output, format=fileending)
        output.seek(0)

        return InMemoryUploadedFile(output, 'ImageField',
                                    "%s.{}".format(fileending) % self.image.name.split('.')[0],
                                    'image/{}'.format(fileending),
                                    sys.getsizeof(output), None)

    def __str__(self):
        return self.name


"""
The Feedback model which represents a feedback can be positive/neutral/negative.
A feedback consts of a Rating (good/bad/ etc.) and also has the Roles of the trader partner, did he receive the pollen or did he send the pollen?
"""


class Rating(models.TextChoices):
    POSITIVE = "1", "positive",
    NEUTRAL = "0", "neutral",
    NEGATIVE = "-1", "negative"


class Role(models.TextChoices):
    Sender = "sender", "Sender",
    Receiver = "receiver", "Receiver",


class Feedback(models.Model):
    page_to_offer = models.URLField(max_length=400)
    buyer = models.CharField(max_length=50)
    seller = models.CharField(max_length=50)
    offered_nepenthes = models.CharField(
        max_length=100)  # this field will be set automaticly after the user created a feedback for an user
    rating = models.CharField(
        max_length=2,
        choices=Rating.choices,
        default=Rating.POSITIVE
    )
    comment = models.CharField(max_length=100)


class Transaction(models.Model):
    author = models.ForeignKey(CustomUser,
                               null=False,
                               on_delete=models.CASCADE,
                               )  # author of the post
    user = models.ForeignKey(CustomUser,
                             null=False,
                             on_delete=models.CASCADE,
                             related_name="user"
                             )  # interested party
    author_plant = models.ForeignKey(Nepenthes, null=False, on_delete=models.CASCADE)
    user_plant = models.ForeignKey(Nepenthes, null=False, on_delete=models.CASCADE, related_name="user_plant")
    accepted = models.BooleanField(null=True)  # does the author accept?
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["author", "user", "author_plant", "user_plant"], name="unique_transaction")]


class Blacklist(models.Model):
    user = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE, related_name="user_id")
    banned_user = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE, related_name="banned_user")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "banned_user"], name="unique_bann")]
