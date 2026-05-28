
def add_credits(user, amount):
    user.credits += amount
    user.save()