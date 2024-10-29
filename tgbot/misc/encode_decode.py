import base64

def encode_string(string):
  """Encodes a string using base64."""
  encoded_bytes = base64.b64encode(string.encode('utf-8'))
  encoded_string = encoded_bytes.decode('utf-8')
  return encoded_string

def decode_string(encoded_string):
  """Decodes a base64-encoded string."""
  decoded_bytes = base64.b64decode(encoded_string.encode('utf-8'))
  decoded_string = decoded_bytes.decode('utf-8')
  return decoded_string


def make_referral_link(username, bloger_id, social_media):
    code = encode_string(f"{bloger_id},{social_media}")
    return f"https://t.me/{username}?start={code}"