import random
from Cryptography import cryptomath

# Pre generated primes
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]


def get_best_choice(bitlength):
    """To check whether the random number is best choice for prime.
    This function will divide random number by all pre generated primes,
    if the number is divide by any of the pre generated prime then it will
    take another random number and check again.
    if number is not divide by any pre generated prime then simply returns that number
    :param bitlength:
    :return best choice for prime number of bitlength:
    """
    while True:
        # random number range should be from 2^1023 + 1 to 2^1024 - 1
        prime_choice = random.randrange(2 ** (bitlength - 1) + 1, 2 ** bitlength - 1)

        for divisor in first_primes_list:
            if prime_choice % divisor == 0:
                break
        else:
            return prime_choice


def is_millar_rabin_passed(prime_choice):
    """Millar Rabin algorithm (Primality test 3) for checking whether the number is prime or not
    (this algorithm specifically used for very large number)
    :param prime_choice:
    :return True for probably prime number otherwise False:
    """
    # find r such that n = 2^u * r + 1
    r = prime_choice - 1
    max_division_by_two = 0

    while r % 2 == 0:
        # divide by two is similar to shift 1 right side
        r >>= 1  # r = r/2
        max_division_by_two += 1
    assert (2 ** max_division_by_two * r == prime_choice - 1)  # 2^u * r == n - 1

    def is_composite(number):
        """This function to check millar rabin conditions whether the number is composite or not:
            (i) a^r mod(n) != 1 Returns True
            (i) i in 0 to u (here max_division_by_two) checking:
                a^(2^i * r) mod(n) != (n - 1) Returns True
        :param number:
        """
        if pow(number, r, prime_choice) == 1:
            return False

        for i in range(max_division_by_two):
            if pow(number, 2 ** i * r, prime_choice) == (prime_choice - 1):
                return False

        return True

    # generally in millar rabin algorithm for finding
    # whether the number is prime or not 20 iteration perform
    no_of_iteration = 20
    # Checks 20 times whether the random number passes millar rabin condition or not
    for _ in range(no_of_iteration):
        tester = random.randrange(2, prime_choice - 2)  # range should be 2 to (prime_choice - 2)
        if is_composite(tester):
            return False

    return True


def generate_prime_number():
    """This function returns probably prime number.
    first it generates the random integer using get_best_choice function
    then it will check whether the number is passed by millar rabin algorithm
    if it returns true then this function returns the probably prime number of length 1024
    """
    while True:
        bitlength = 1024
        prime_choice = get_best_choice(bitlength)

        if not is_millar_rabin_passed(prime_choice):
            continue
        else:
            return prime_choice


def generate_key_pair():
    """Generate public key and private key pair
    public key is pair of e (which is co-prime of n) and
    n(which is multiplication of two prime numbers (p,q))

    private key is pair of d(which is multiplicative inverse of e) and n

    :return (public key, private key):
    """
    p = generate_prime_number()
    q = generate_prime_number()

    n = p * q
    phi = (p - 1) * (q - 1)

    while True:
        e = random.randrange(1, phi)
        if cryptomath.gcd(e, phi) == 1:
            break

    d = cryptomath.mod_inverse(e, phi)

    return (e, n), (d, n)
