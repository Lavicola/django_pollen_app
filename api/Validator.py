from rest_framework.exceptions import ValidationError

from pollen_app.models import Nepenthes
from user.models import CustomUser



def validate_transaction(interested_person_id, user_plant_id, author, author_plant_id):
    #the id must be an int
    try:
        user_plant_id = int(user_plant_id)
        author_plant_id = int(author_plant_id)
    except ValueError as e:
        raise ValidationError("plant id must be an int")

    # exactly one user must exist
    author = CustomUser.objects.filter(username=author)
    if(len(author) != 1):
        raise ValidationError("User must be exactly one")
    # author plant must belong to the author
    author_plant = Nepenthes.objects.filter(owner_id=author[0].id,id=author_plant_id)
    if (len(author_plant) != 1):
        raise ValidationError("author plant does not exist!")
    #user plant must belong to the user
    user_plant = Nepenthes.objects.filter(owner_id=interested_person_id, id=user_plant_id)
    if (len(user_plant) != 1):
        raise ValidationError("user plant does not exist!")
    #TODO reduce the amount of SQL Statements!
    return author[0].id
