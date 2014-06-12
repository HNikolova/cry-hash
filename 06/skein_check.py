# ------------------------------------------------------------------------------
#
#                Solution by Felix Lauer & Simon Schneegans
#
# ------------------------------------------------------------------------------
def rotate_right64(x, n):
    mask = (2L**n) - 1
    mask_bits = x & mask
    return (x >> n) | (mask_bits << (64 - n))

def rotate_left64(x, n):
    return rotate_right64(x, 64 - n)

def count_ones_without_msb64(block):
  count = 0
  for i in range(0,63):
     if block & 2**i > 0:
      count += 1
  return count

def skein_round(block0, block1, block2, block3, rotation_value):

  # MIX

  # We substitute the addition by xor to not introduce carry bits into the
  # differences. We accumulate the probability of no carry bits being
  # introduced by the addition of the message blocks.
  block0 = block0^block1

  block1 = rotate_left64(block1, rotation_value) ^ block0

  block2 = block2^block3

  block3 = rotate_left64(block3, rotation_value) ^ block2

  # PERMUTE
  return (block2, block1, block0, block3)

# ------------------------------------------------------------------------------
if __name__ == '__main__':
  results = []

  for block_num in range(0, 4):
    for diff in range(0, 64):
      for rot_const in range(1, 63):
        block0 = 1 << diff if block_num is 0 else 0
        block1 = 1 << diff if block_num is 1 else 0
        block2 = 1 << diff if block_num is 2 else 0
        block3 = 1 << diff if block_num is 3 else 0

        probability = 1
        max_round = 0

        for round_num in range(0, 72):
          one_count = count_ones_without_msb64(block0)
          one_count += count_ones_without_msb64(block1)
          one_count += count_ones_without_msb64(block2)
          one_count += count_ones_without_msb64(block3)

          probability *=  2**-one_count

          if probability < 2**-255:
            break

          (block0, block1, block2, block3) = skein_round(block0, block1, block2, block3, rot_const)
          max_round += 1

        results.append((probability, max_round, rot_const, block_num * 64 + diff))

      print "Percentage of differences checked: " + str((block_num * 64 + diff + 1) * 100 / 256)

  sorted_results = sorted(results, key=lambda item: -item[0])

  # Print the top 100 results, beginning with the highest differential path probability
  for i in range(0, 100):
    print "Pobability: ", sorted_results[i][0], " | Path length: ", sorted_results[i][1], " | Rotational constant: ", sorted_results[i][2], " | Position of 1bit in input difference: ", sorted_results[i][3]



























