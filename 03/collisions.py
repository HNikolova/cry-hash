# ------------------------------------------------------------------------------
#
#                Solution by Felix Lauer & Simon Schneegans
#
#             run "python collisions.py --help" for usage hints
# ------------------------------------------------------------------------------

import hashlib, random, string, time, argparse

# ------------------------------------------------------------------------------
# returns a random string with "length" characters
def get_random_string(length):
  return ''.join(random.choice(string.letters.join(string.digits)) for i in range(length))


# ------------------------------------------------------------------------------
# computes the sha512 for the given message and returns the first k bytes
def get_truncated_hash(message, k):
  return hashlib.sha512(message).digest()[-k:]


# ------------------------------------------------------------------------------
# helper method for pretty search result printing
def print_results(m0, m1, hash, k):
  print "Message A:", m0.encode("hex")   # encode to human-readable hex values
  print "Message B:", m1.encode("hex")
  print "Same hash:", hash.encode("hex")


# ------------------------------------------------------------------------------
# searches for k-byte collisions with the birthday attack. if a dp_pattern is
# provided, only hashes ending with those bytes will be considered
def simple_birthday(k, dp_pattern):

  hash_table  = dict()
  len_pattern = len(dp_pattern)

  while True:
    s    = get_random_string(k)
    hash = get_truncated_hash(s, k)

    if hash[k-len_pattern+1:k].encode("hex") == dp_pattern:
      if hash in hash_table:
        if hash_table[hash] != s:
          print_results(s, hash_table[hash], hash, k)
          break
      else:
        hash_table[hash] = s


# ------------------------------------------------------------------------------
# searches for k-byte collisions with floyd cycle finding
# based on http://en.wikipedia.org/wiki/Cycle_detection
def floyd(k):

  x0 = get_random_string(k)
  m0 = None
  m1 = None

  turtle = get_truncated_hash(x0, k)
  hare   = get_truncated_hash(turtle, k)

  while turtle != hare:
    turtle = get_truncated_hash(turtle, k)
    hare   = get_truncated_hash(get_truncated_hash(hare, k), k)

  pre_period_length = 0
  turtle = x0
  while turtle != hare:
    m0     = turtle
    turtle = get_truncated_hash(turtle, k)
    hare   = get_truncated_hash(hare, k)
    pre_period_length += 1

  if pre_period_length is 0:
    print "Failed to find a collision: x0 was in a cycle!"
    return

  period_length = 1
  hare = get_truncated_hash(turtle, k)
  while turtle != hare:
    m1   = hare
    hare = get_truncated_hash(hare, k)
    period_length += 1

  print_results(m0, m1, get_truncated_hash(m0, k), k)


# ------------------------------------------------------------------------------
# searches for k-byte collisions with brent cycle finding
# based on http://en.wikipedia.org/wiki/Cycle_detection
def brent(k):

  x0 = get_random_string(k)
  m0 = None
  m1 = None

  turtle = x0
  hare   = get_truncated_hash(turtle, k)
  power  = period_length = 1

  while turtle != hare:
    if power == period_length:
      turtle = hare
      power *= 2
      period_length = 0
    hare = get_truncated_hash(hare, k)
    period_length += 1


  pre_period_length = 0
  turtle = hare = x0
  for i in range(period_length):
    hare = get_truncated_hash(hare, k)

  while turtle != hare:
    m0 = turtle
    m1 = hare
    turtle = get_truncated_hash(turtle, k)
    hare   = get_truncated_hash(hare, k)
    pre_period_length += 1

  if pre_period_length is 0:
    print "Failed to find a collision: x0 was in a cycle!"
    return

  print_results(m0, m1, get_truncated_hash(m0, k), k)


# ------------------------------------------------------------------------------
# executes one of the above, based on "mode"
def search_near_collision(mode, bytes, pattern):
  if mode == "birthday":
    simple_birthday(bytes, pattern)
  elif mode == "floyd":
    floyd(bytes)
  elif mode == "brent":
    brent(bytes)

# ------------------------------------------------------------------------------
if __name__ == '__main__':

  # add command line options
  parser = argparse.ArgumentParser(description='Search for near collisions of sha512.')
  parser.add_argument('-k', metavar="BYTES", default=4, type=int, help='Amount of bytes which shall collide. Use a value of -1 to start a infinite search for a large k.')
  parser.add_argument('-m', default="floyd", choices=["birthday", "floyd", "brent"], help='The algorithm used.')
  parser.add_argument('-p', metavar="PATTERN", default="", help='A hex-pattern defining distinguished points for the birthday algorithm.')
  parser.add_argument('-s', metavar="SAMPLES", default=1, type=int, help='Amount of repetitions performed, for time averaging.')
  args = parser.parse_args()

  # search mode
  if args.k == -1:
    k = 3

    while True:
      start = time.time()
      print "Searching a collision for k =",k,"..."
      search_near_collision(args.m, k, args.p)
      print "Time taken:", (time.time() - start)/args.s
      print ""

      k += 1

  # profile mode
  else:
    start = time.time()
    for i in range(args.s):
      search_near_collision(args.m, args.k, args.p)
      print ""

    print "-----------------------------------"
    print "Time per collisions:     ", (time.time() - start)/args.s

# b) average time (20 samples) per 5 byte-collision
# birthday: 23.8 s
# floyd:     4.9 s
# brent:     3.8 s

# c)
# floyd
# -------- k = 8 ----------
# Message A: cd2c68d43b50968a
# Message B: e80449ba1b1c7f4a
# Same hash: 45491f36ca056b40
# Time taken: 34412.193804

# Message A: ff9649cb549be024
# Message B: 6d52e680318ce06a
# Same hash: d2eb5d170f3dbead
# Time taken: 27141.8880491

# Message A: c70cf4c6a85595e0
# Message B: 8be877564e2a3323
# Same hash: 7a8245bce35a679c
# Time taken: 3488.26078105

# -------- k = 8 ----------
# Message A: 8f167e92c22154dd
# Message B: 2713a9e73bc80ffb
# Same hash: aa601227397e64d8
# Time taken: 15397.762315

# brent
# -------- k = 7 ----------
# Message A: 9ed22ca449dc2a
# Message B: c895d52df1c3f3
# Same hash: 8e682596c5c09e
# Time taken: 603.337014914

# Message A: e25b4f6562ce9a
# Message B: e1e261f583cd76
# Same hash: b2134f793f8971
# Time taken: 809.815823078

# Message A: 55f748b8e558d3
# Message B: 4c0653dbdfe631
# Same hash: 5f4024facbcc1f
# Time taken: 1156.3751359

# birthday with pattern "00"
# -------- k = 7 ----------
# Message A: 56537878756442
# Message B: 59794644464945
# Same hash: 2dc3b3d95d6900
# Time taken: 123741.494141





