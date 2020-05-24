from random import SystemRandom
import hashlib
import codecs
import hmac
import sys

_sys_rng = SystemRandom()
SALT_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
DEFAULT_PBKDF2_ITERATIONS = 150000

_builtin_safe_str_cmp = getattr(hmac, "compare_digest", None)

def pbkdf2_hex(data, salt, iterations=DEFAULT_PBKDF2_ITERATIONS, keylen=None, hashfunc=None):
    rv = pbkdf2_bin(data, salt, iterations, keylen, hashfunc)
    return codecs.encode(rv, "hex_codec").decode("ascii")
def pbkdf2_bin(data, salt, iterations=DEFAULT_PBKDF2_ITERATIONS, keylen=None, hashfunc=None):
    if not hashfunc:
        hashfunc = "sha256"

    data = _to_bytes(data)
    salt = _to_bytes(salt)

    if callable(hashfunc):
        _test_hash = hashfunc()
        hash_name = getattr(_test_hash, "name", None)
    else:
        hash_name = hashfunc
    return hashlib.pbkdf2_hmac(hash_name, data, salt, iterations, keylen)
def gen_salt(length):
    """Generate a random string of SALT_CHARS with specified ``length``."""
    if length <= 0:
        raise ValueError("Salt length must be positive")
    return "".join(_sys_rng.choice(SALT_CHARS) for _ in range(length))

def _hash_internal(method, salt, password):
    if method == "plain":
        return password, method

    if isinstance(password, str):
        password = password.encode("utf-8")

    if method.startswith("pbkdf2:"):
        args = method[7:].split(":")
        if len(args) not in (1, 2):
            raise ValueError("Invalid number of arguments for PBKDF2")
        method = args.pop(0)
        iterations = int(args[0] or 0) if args else DEFAULT_PBKDF2_ITERATIONS
        is_pbkdf2 = True
        actual_method = f"pbkdf2:{method}:{iterations}"
    else:
        is_pbkdf2 = False
        actual_method = method

    if is_pbkdf2:
        if not salt:
            raise ValueError("Salt is required for PBKDF2")
        rv = pbkdf2_hex(password, salt, iterations, hashfunc=method)
    elif salt:
        if isinstance(salt, str):
            salt = salt.encode("utf-8")
        mac = _create_mac(salt, password, method)
        rv = mac.hexdigest()
    else:
        rv = hashlib.new(method, password).hexdigest()
    return rv, actual_method

def _create_mac(key, msg, method):
    if callable(method):
        return hmac.HMAC(key, msg, method)

    def hashfunc(d=b""):
        return hashlib.new(method, d)

    return hmac.HMAC(key, msg, hashfunc)

def generate_password_hash(password, method="pbkdf2:sha256", salt_length=8):
    salt = gen_salt(salt_length) if method != "plain" else ""
    h, actual_method = _hash_internal(method, salt, password)
    return f"{actual_method}${salt}${h}"

def check_password_hash(pwhash, password):
    if pwhash.count("$") < 2:
        return False
    method, salt, hashval = pwhash.split("$", 2)
    return safe_str_cmp(_hash_internal(method, salt, password)[0], hashval)

def safe_str_cmp(a, b):
    if isinstance(a, str):
        a = a.encode("utf-8")
    if isinstance(b, str):
        b = b.encode("utf-8")

    if _builtin_safe_str_cmp is not None:
        return _builtin_safe_str_cmp(a, b)

    if len(a) != len(b):
        return False

    rv = 0
    for x, y in zip(a, b):
        rv |= x ^ y

    return rv == 0

def _to_bytes(x, charset=sys.getdefaultencoding(), errors="strict"):  # noqa: B008
    if x is None or isinstance(x, bytes):
        return x

    if isinstance(x, (bytearray, memoryview)):
        return bytes(x)

    if isinstance(x, str):
        return x.encode(charset, errors)

    raise TypeError("Expected bytes")