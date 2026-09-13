import hashlib

def generate_unique_id(data):
    
    encoded_data = data.lower().strip().encode('utf-8')
    unique_hash = hashlib.md5(encoded_data).hexdigest()[:8].upper()
    
    return f"{unique_hash[:4]}-{unique_hash[4:]}"