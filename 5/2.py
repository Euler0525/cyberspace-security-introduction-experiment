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
            n = p * q                         # n
            tmp = (p - 1) * (q - 1)
            if gmpy2.gcd(n, tmp) == 1:
                break
        g = n + 1                             # g
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

    def add(self, ciphertext1: gmpy2.mpz, ciphertext2: gmpy2.mpz) -> gmpy2.mpz:
        n, g = self.pubkey
        ciphertext = (ciphertext1 * ciphertext2) % (n ** 2)

        return ciphertext


def main():
    """Paillier算法在电子投票中的应用"""
    print("******************************************此程序模拟了基于Paillier算法的匿名电子投票的流程************************************************************")
    print("首先每位投票者为候选人投票并将结果加密发送给计票人，每人只有一张选票，选票上被投票的候选者得到一张选票，其他后选择得到0张选票；")
    print("然后计票人将所有选票上对应候选人的加密的投票结果相乘，并将加密的统计结果发送给公布人；")
    print("最后公布人对统计的票数进行解密并公布。")
    print("******************************************************************************************************************************************************")
    candidate_num = int(input("请设置候选者人数："))
    voter_num = int(input("请设置投票者人数："))
    homo = HomomorphicEncryption()
    ballots = []  # 存储选票的二维列表

    # 开始计票
    for i in range(voter_num):
        print(
            f"\n--------------------------------------------------------------请第{i+1}位投票者为候选者投票---------------------------------------------------------------")
        ballots.append([])
        for j in range(candidate_num):
            ballot = int(input(f"请为第{j+1}位候选者投票："))
            ballots[i].append(homo.encrypt(ballot))

    print("\n对该投票结果进行加密并发送给计票人；")
    encrypted_ballots = []
    for j in range(candidate_num):
        ballot = homo.encrypt(0)
        for i in range(voter_num):
            ballot = homo.add(ballot, ballots[i][j])
        encrypted_ballots.append(ballot)
    print("计票人对此投票结果进行计票。")
    print("----------------------------------------------------计票人计票完成并将加密后的投票结果发送给公布人----------------------------------------------------")
    print("加密后的投票结果为：")

    for i in range(candidate_num):
        print(f"第{i+1}为候选者获得的选票票数的加密结果为：{encrypted_ballots[i]}\n")

    print("--------------------------------------------------------公布人解密计票结果并公布最终的投票结果--------------------------------------------------------")
    result = []
    for i in range(candidate_num):
        c = homo.decrypt(encrypted_ballots[i])
        result.append(c)
        print(f"第{i+1}位候选者获得了{c}张票；")

    # 找到最大值的他的索引
    max_value = max(result)
    max_index = [i + 1 for i, v in enumerate(result) if v == max_value]
    print(f"最终第{max_index}位候选人获得的选票最多，为{max_value}张")


if __name__ == "__main__":
    main()
