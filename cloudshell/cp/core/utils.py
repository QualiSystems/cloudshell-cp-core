from io import StringIO

import paramiko


def generate_ssh_key_pair(bits=2048):
    """Generate SSH key pair

    :param int bits:
    :rtype: tuple[str, str]
    """
    key = paramiko.RSAKey.generate(bits)
    public_key = f"{key.get_name()} {key.get_base64()}"
    private_key = StringIO()
    key.write_private_key(private_key)
    private_key.seek(0)

    return private_key.read(), public_key
