import re

class ValidationError(Exception):
    pass

def validate_user(data):
    errors = []
    
    if not data.get('name') or not data['name'].strip():
        errors.append(f"Row {data.get('id')}: Name is required")
    
    email = data.get('email', '')
    if not email or not email.strip():
        errors.append(f"Row {data.get('id')}: Email is required")
    else:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            errors.append(f"Row {data.get('id')}: Invalid email format")
    
    if errors:
        raise ValidationError('; '.join(errors))
    
    return True

def validate_product(data):
    errors = []
    
    if not data.get('name') or not data['name'].strip():
        errors.append(f"Row {data.get('id')}: Product name is required")
    
    try:
        price = float(data.get('price', 0))
        if price < 0:
            errors.append(f"Row {data.get('id')}: Price cannot be negative")
    except (ValueError, TypeError):
        errors.append(f"Row {data.get('id')}: Invalid price format")
    
    if errors:
        raise ValidationError('; '.join(errors))
    
    return True

def validate_order(data):
    errors = []
    
    if not data.get('user_id'):
        errors.append(f"Row {data.get('id')}: User ID is required")
    
    if not data.get('product_id'):
        errors.append(f"Row {data.get('id')}: Product ID is required")
    
    try:
        quantity = int(data.get('quantity', 0))
        if quantity <= 0:
            errors.append(f"Row {data.get('id')}: Quantity must be greater than 0")
    except (ValueError, TypeError):
        errors.append(f"Row {data.get('id')}: Invalid quantity format")
    
    if errors:
        raise ValidationError('; '.join(errors))
    
    return True
