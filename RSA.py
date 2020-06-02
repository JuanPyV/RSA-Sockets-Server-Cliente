import random


class RSA:
    def __init__(self):
        super().__init__()

    @staticmethod
    def generateKeys():
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
                  71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149,
                  151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
                  233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313,
                  317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
                  419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
                  503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601,
                  607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691,
                  701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809,
                  811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907,
                  911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
        p = random.choice(primes)
        q = random.choice(primes)
        while p == q:
            q = random.choice(primes)
        n = p * q
        m = (p - 1) * (q - 1)  # cantidad de coprimos / m es phi
        e = random.randint(0, m)  # llave publica
        while MCD(e, m) != 1:  # e tiene que ser un numero que pertenezca a los coprimos de n y el MCD sea 1

            e = random.randint(1, m)
        i = 1
        while i < m:
            valor = (e * i) % m
            if valor == 1:
                d = i  # calculamos llave privada
                break
            i = i + 2
        publicKey = [n, e]
        privateKey = [n, d]
        return [publicKey, privateKey]

    @staticmethod
    def encrypt(message, publicKey):
        encryptedMessage = []
        for c in message:
            y = pow(ord(c), publicKey[1], publicKey[0])
            encryptedMessage.append(y)
        encryptedMessageString = ",".join(str(x) for x in encryptedMessage)
        return encryptedMessageString

    @staticmethod
    def deEncrypt(encryptedMessageString, privateKey):
        encryptedMessage = encryptedMessageString.split(",")
        for c in encryptedMessage:
            encryptedMessage[c] = int(encryptedMessage[c])
        deEncryptedMessage = []
        for i in range(len(encryptedMessage)):
            variable2 = pow(encryptedMessage[i], privateKey[1], privateKey[0])
            variable1 = chr(variable2)
            deEncryptedMessage.append(variable1)
        deEncryptedMessageString = "".join(str(x) for x in deEncryptedMessage)
        return deEncryptedMessageString


def exponenciarRapido(x, e, m):
    X = x
    E = e
    Y = 1
    while E > 0:
        if E % 2 == 0:
            X = (X * X) % m
            E = E / 2
        else:
            Y = (X * Y) % m
            E = E - 1
    return Y


def MCD(n1, n2):
    while n1 != n2:
        if n1 > n2:
            n1 = n1 - n2
        else:
            n2 = n2 - n1
    return n1

