import time
import base64
import hmac
import uuid

key = "F2432A13U45D24E64C"

def generate_token(expire=3600):
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1 = hmac.new(key.encode("utf-8"), ts_byte, "sha1").hexdigest()
    token = ts_str + ":" + sha1
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")

def verify_token(token):
    token_str = base64.urlsafe_b64decode(token).decode("utf-8")
    token_list = token_str.split(":")
    if len(token_list) != 2:
        return False
    ts_str = token_list[0]
    print(token_list)
    if float(ts_str) < time.time():
        return False
    
    know_sha1_tsstr = token_list[1]
    sha1 = hmac.new(key.encode("utf-8"), ts_str.encode("utf-8"), "sha1")
    calc_sha1_tsstr = sha1.hexdigest()
    if calc_sha1_tsstr != know_sha1_tsstr:
        return False
    return True


# token = generate_token(3600)
# print(token)
# result = verify_token(token)
# print(result)