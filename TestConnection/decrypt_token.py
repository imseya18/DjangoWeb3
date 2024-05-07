from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import json
from cryptography.hazmat.primitives import serialization
import base64
from django.conf import settings
from .loger_config import setup_logger

logger = setup_logger(__name__)


def load_public_key(filename):
    with open(filename, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
        )
    return public_key


def decrypt(message, signature, public_key):
    try:
        json_data = json.dumps(message)
        data_bytes = json_data.encode('utf-8')
        signature_bytes = base64.b64decode(signature)
        public_key.verify(
            signature_bytes,
            data_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        logger.info("Token is valid")
        return True
    except Exception as e:
        logger.warn("Invalid token")
        return False


def decrypt_routine(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return False
    if not decrypt(request.data, auth_header, settings.API_PUBLIC_KEY):
        return False
    return True

