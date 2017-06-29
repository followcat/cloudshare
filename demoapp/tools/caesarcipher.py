def encrypt(n, plaintext, key='1234567890'):
    result = ''

    for l in plaintext:
        try:
            i = (key.index(l) + n) % 10
            result += key[i]
        except ValueError:
            result += l

    return result


def decrypt(n, ciphertext, key='1234567890'):
    result = ''

    for l in ciphertext:
        try:
            i = (key.index(l) - n) % 10
            result += key[i]
        except ValueError:
            result += l

    return result


def show_result(plaintext, n, key='1234567890'):
    """
        >>> from demoapp.tools.caesarcipher import *
        >>> origin = '1234567890abcdefghijklmnopqrstuvwxyz'
        >>> e1 = encrypt(1, origin)
        '2345678901abcdefghijklmnopqrstuvwxyz'
        >>> e2 = encrypt(3, origin)
        '4567890123abcdefghijklmnopqrstuvwxyz'
        >>> assert(origin == decrypt(1, e1))
        >>> assert(origin == decrypt(3, e1))
    """
    encrypted = encrypt(n, plaintext, key)
    decrypted = decrypt(n, encrypted, key)

    print('Rotation: %s' % n)
    print('Plaintext: %s' % plaintext)
    print('Encrytped: %s' % encrypted)
    print('Decrytped: %s' % decrypted)
