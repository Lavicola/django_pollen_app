from rest_framework.exceptions import ValidationError

from pollen_app.models import Nepenthes, Blacklist
from user.models import CustomUser


def validate_transaction(interested_person_id, user_plant_id, author, author_plant_id):
    # the id of the plants must be an int
    try:
        user_plant_id = int(user_plant_id)
        author_plant_id = int(author_plant_id)
    except ValueError as e:
        raise ValidationError("plant id must be an int")

    # exactly one user must exist
    author = CustomUser.objects.filter(username=author)
    if (author.count() != 1):
        raise ValidationError("User must be exactly one")
    author_id = author[0].id
    # author plant must belong to the author
    author_plant = Nepenthes.objects.filter(owner_id=author_id, id=author_plant_id)
    if (author_plant.count() != 1):
        raise ValidationError("author plant does not exist!")
    # user plant must belong to the user
    user_plant = Nepenthes.objects.filter(owner_id=interested_person_id, id=user_plant_id)
    if (user_plant.count() != 1):
        raise ValidationError("user plant does not exist!")

    # TODO check if user is banned
    #blacklist_validator(author_id, interested_person_id)

    return author_id


def blacklist_validator(user_id, banned_user_id):
    if Blacklist.objects.filter(banned_user_id=banned_user_id, user_id=user_id).count() > 0:
        raise ValidationError("plant id must be an int")
