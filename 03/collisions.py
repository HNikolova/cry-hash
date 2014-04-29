import hashlib
import random
import string
import time

def random_string(length):
   return ''.join(random.choice(string.letters.join(string.digits)) for i in range(length))

start = time.time()
k = 13
hash_table = dict()

while True:
    s = random_string(15)
    hash = hashlib.sha512(s).hexdigest()[:k]

    if hash in hash_table:
        if hash_table[hash] is not s:
            print "Found a collision for k =",k,"!"
            print "------------------------------"
            print "Message A:", s
            print "Message B:", hash_table[hash]
            print "Hash:     ", hash
            break
    else:
        hash_table[hash] = s
        l = len(hash_table)

        if l % 10000 == 0:
            print "Tried " + str(l/1000) + "k different messages ..."

print "Time:     ", time.time() - start


# Found a collision for k = 12 !
# ------------------------------
# Message A: nHimKpiCgYaCqrz
# Message B: XeXEHCUoInRdFay
# Hash:      efb27b086b22
# Time:      201.337332964
