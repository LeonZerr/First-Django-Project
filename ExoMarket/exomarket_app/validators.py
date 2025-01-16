from django.core.exceptions import ValidationError


def validate_phone_number(value):
    if not value.isdigit():
        raise ValidationError("Phone Number can only contain integers.")    
    
    if len(value) < 10:
        raise ValidationError("Number must contain at least 10 numbers.")



def validate_price(value):
    if value <= 0:
        raise ValidationError("Price must be positive.")
    
    
    
def validate_forbidden_words(value):
    BAD_WORDS = [
        'harry potter', 'frodo baggins', 'bilbo baggins', 'gandalf', 'dumbledore', 'voldemort', 
        'luke skywalker', 'darth vader', 'spider-man', 'superman', 'batman', 'wonder woman'
    ]
    
    if any([word in value.lower() for word in BAD_WORDS]):
        raise ValidationError('Content contains bad words or phrases')



def validate_quantity(value):
    if value <= 0:
        raise ValidationError("Quantity must be positive.")
   