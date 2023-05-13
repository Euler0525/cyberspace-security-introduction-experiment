import time
import gmpy2
import libnum


class Paillier(object):
    def __init__(self, pubkey=None, privkey=None):
        self.pubkey = pubkey
        self.privkey = privkey
        self.genKey()

    def encrypt(self, plaintext: int) -> gmpy2.mpz:
        n, g = self.pubkey
        # 基于时间生成随机数, 满足 $r \in Z_{n^2}^*$
        r = gmpy2.mpz_random(gmpy2.random_state(int(time.time())), n)
        while gmpy2.gcd(r, n) != 1:
            r = gmpy2.mpz_random(gmpy2.random_state(int(time.time())), n)

        ciphertext = gmpy2.powmod(g, plaintext, n ** 2) * \
            gmpy2.powmod(r, n, n ** 2) % (n ** 2)

        return ciphertext

    def decrypt(self, ciphertext: gmpy2.mpz) -> int:
        n, g = self.pubkey
        la, mu = self.privkey
        tmp = gmpy2.powmod(ciphertext, la, n ** 2)
        tmp = gmpy2.mpz(self.lx(tmp, n))
        tmp = tmp * mu % n
        plaintext = int(tmp)

        return plaintext

    def genKey(self):
        """随机生成公私钥对"""
        # 生成两个1024位大素数p, q满足gcd(pq,(p-1)(q-1))=1
        while True:
            p = self.genPrime()
            q = self.genPrime()
            n = p * q                        # n
            tmp = (p - 1) * (q - 1)
            if gmpy2.gcd(n, tmp) == 1:
                break
        g = n + 1                            # g
        la = tmp // gmpy2.gcd(p - 1, q - 1)  # \lambda
        tmp = gmpy2.powmod(g, la, n ** 2)
        tmp = gmpy2.mpz(self.lx(tmp, n))
        mu = gmpy2.invert(tmp, n)            # \mu

        self.pubkey = (n, g)
        self.privkey = (la, mu)

    def genPrime(self) -> gmpy2.mpz:
        """随机生成1024位的素数"""
        tmp = libnum.generate_prime(1024)
        p = gmpy2.mpz(tmp)

        return p

    def lx(self, x: gmpy2.mpz, n: gmpy2.mpz) -> gmpy2.mpz:
        return (x - 1) // n


class HomomorphicEncryption(Paillier):
    def __init__(self):
        super(HomomorphicEncryption, self).__init__(pubkey=None, privkey=None)
        self.genKey()

    """
    - 同态加：对于密文$c_1$和$c_2$，计算$c=c_1 \cdot c_2 \bmod n ^ 2$，明文实现$m_1 + m_2$;
    - 同态标量乘：对于密文$c_1$和标量$a$，计算$c=c_1^a \bmod n^2$，明文实现$a\cdot m1$;
    """

    def add(self, plaintext1: int, plaintext2: int) -> gmpy2.mpz:
        """同态加运算"""
        n, g = self.pubkey
        ciphertext1 = self.encrypt(plaintext1)
        print("对第一个明文加密后结果为：")
        print(ciphertext1)
        ciphertext2 = self.encrypt(plaintext2)
        print("对第二个明文加密后结果为：")
        print(ciphertext2)
        ciphertext = (ciphertext1 * ciphertext2) % (n ** 2)
        print("两密文相乘得到：")
        print(ciphertext)

        return ciphertext

    def scalarMul(self, a: int, plaintext: int) -> gmpy2.mpz:
        """同态标量乘运算"""
        n, g = self.pubkey
        ciphertext = self.encrypt(plaintext)
        print("对明文加密后得到密文：", end="")
        print(ciphertext)
        ciphertext = gmpy2.powmod(ciphertext, a, n ** 2)
        print(f"密文的{a}次幂得到", end="")
        print(ciphertext)

        return ciphertext


def main():
    print("******************************************************************************************************************************************************")
    print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓验证加法的同态性↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓")
    m1 = int(input("请输入第一个明文："))
    m2 = int(input("请输入第二个明文："))
    homo = HomomorphicEncryption()
    c = homo.add(m1, m2)
    p = homo.decrypt(c)
    print("密文相乘后解密得到的明文为：", end="")
    print(p)
    print("******************************************************************************************************************************************************")
    print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓验证标量乘法的同态性↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓")
    a = int(input("请输入标量："))
    m = int(input("请输入明文："))
    homo = HomomorphicEncryption()
    c = homo.scalarMul(a, m)
    p = homo.decrypt(c)
    print(f"密文的{a}次幂后解密得到的明文为：", end="")
    print(p)
    print("******************************************************************************************************************************************************")


if __name__ == "__main__":
    main()
