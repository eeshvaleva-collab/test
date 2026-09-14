import hashlib

def generate_id(data):
    encoded_data = data.lower().strip().encode("utf-8")
    hash_value = hashlib.md5(encoded_data).hexdigest()[:8]

    return f"{hash_value[:4]}-{hash_value[4:]}"