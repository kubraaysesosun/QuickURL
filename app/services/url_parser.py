import hashlib
import base64
import uuid

SHORT_URL_LENGTH = 6


def generate_short_url(original_url: str, length: int = SHORT_URL_LENGTH) -> str:

    data_to_hash = original_url + str(uuid.uuid4())
    hash_value = hashlib.sha256(data_to_hash.encode()).digest()

    return base64.urlsafe_b64encode(hash_value).decode()[:length]

