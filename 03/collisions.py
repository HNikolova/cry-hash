import hashlib
import random
import string
import time

def get_random_string(length):
  return ''.join(random.choice(string.letters.join(string.digits)) for i in range(length))

def get_truncated_hash(message, k):
  return hashlib.sha512(message).digest()[:k]

def print_results(m0, m1, hash, k):
  print "Found a collision for k =",k,"!"
  print "------------------------------"
  print "Message A:", m0.encode("hex")
  print "Message B:", m1.encode("hex")
  print "Hash:     ", hash.encode("hex")

# ------------------------------------------------------------------------------
def memory_intense_method(k, dp_pattern):

  hash_table = dict()
  len_pattern = len(dp_pattern)

  while True:
    s = get_random_string(15)
    hash = get_truncated_hash(s, k)

    if hash[k-len_pattern+1:k].encode("hex") == dp_pattern:
      if hash in hash_table:
        if hash_table[hash] is not s:
          print_results(s, hash_table[hash], hash, k)
          break
      else:
        hash_table[hash] = s

# ------------------------------------------------------------------------------
# based on http://en.wikipedia.org/wiki/Cycle_detection
# ------------------------------------------------------------------------------
def floyd(k):

  x0 = get_random_string(k)
  m0 = None
  m1 = None

  tortoise = get_truncated_hash(x0, k)
  hare     = get_truncated_hash(tortoise, k)

  while tortoise != hare:
    tortoise = get_truncated_hash(tortoise, k)
    hare     = get_truncated_hash(get_truncated_hash(hare, k), k)

  pre_period_length = 0
  tortoise = x0
  while tortoise != hare:
    m0       = tortoise
    tortoise = get_truncated_hash(tortoise, k)
    hare     = get_truncated_hash(hare, k)
    pre_period_length += 1

  if pre_period_length is 0:
    print "Failed to find a collision: x0 was in a cycle!"
    return

  period_length = 1
  hare = get_truncated_hash(tortoise, k)
  while tortoise != hare:
    m1   = hare
    hare = get_truncated_hash(hare, k)
    period_length += 1

  print_results(m0, m1, get_truncated_hash(m0, k), k)


# ------------------------------------------------------------------------------
# based on http://en.wikipedia.org/wiki/Cycle_detection
# ------------------------------------------------------------------------------
def brent(k):

  x0 = get_random_string(k)
  m0 = None
  m1 = None

  tortoise = x0
  hare     = get_truncated_hash(tortoise, k)
  power    = period_length = 1

  while tortoise != hare:
    if power == period_length:
      tortoise = hare
      power *= 2
      period_length = 0
    hare = get_truncated_hash(hare, k)
    period_length += 1

  pre_period_length = 0
  tortoise = hare = x0
  for i in range(period_length):
    hare = get_truncated_hash(hare, k)

  while tortoise != hare:
    m0 = tortoise
    m1 = hare
    tortoise = get_truncated_hash(tortoise, k)
    hare     = get_truncated_hash(hare, k)
    pre_period_length += 1

  if pre_period_length is 0:
    print "Failed to find a collision: x0 was in a cycle!"
    return

  print_results(m0, m1, get_truncated_hash(m0, k), k)


# ------------------------------------------------------------------------------
if __name__ == '__main__':

  samples = 1
  k = 4

  start = time.time()

  for i in range(samples):
    memory_intense_method(k, "4f")
    # floyd(k)
    # brent(k)

  print "Time:     ", (time.time() - start)/samples


# memory_intense:
# Found a collision for k = 12 !
# ------------------------------
# Message A: nHimKpiCgYaCqrz
# Message B: XeXEHCUoInRdFay
# Hash:      efb27b086b22
# Time:      201.337332964

# floyd:
# Found a collision for k = 12 !
# ------------------------------
# Message A: 5190d909b193
# Message B: 5c5a8ef4fc33
# Hash:      3a601b099b1c
# Time:      88.8097798824

# brent
# Found a collision for k = 12 !
# ------------------------------
# Message A: 5190d909b193
# Message B: 5c5a8ef4fc33
# Hash:      3a601b099b1c
# Time:      80.675563097
