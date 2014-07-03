#!/usr/bin/python

import sys
import operator
import re
import math

def get_total_count(counts):
  total_count = 0

  for count in counts:
    total_count += count

  return total_count

def get_shannon_entropy(counts):
  entropy = 0
  total_count = get_total_count(counts)
  for count in counts:
    p = 1.0 * count/total_count
    entropy -= p * math.log(p, 2)

  return entropy

def get_min_entropy(counts):
  entropy = 0
  total_count = get_total_count(counts)
  max_count = 0
  for count in counts:
    max_count = max(max_count, count)

  p = 1.0 * max_count/total_count
  entropy = -math.log(p, 2)
  return entropy

def compute_entropies(filename):
  file=open(filename,"r+")
  letter_count={}

  for w in file.read().split():
    word = re.sub("[\, \- \.]+", "", w.strip())
    if len(word) > 0:
      initial = word[0]
      if initial.isalpha():
        if initial not in letter_count:
          letter_count[initial] = 1
        else:
          letter_count[initial] += 1

  sorted_letters = sorted(letter_count.iteritems(), key=operator.itemgetter(1))
  sorted_letter_count = sorted(letter_count.values())
  file.close();

  total_count = get_total_count(sorted_letter_count)
  print "Task a)"
  print ""
  print "Processing file", filename
  print ""
  print "Shannon entropy: ", get_shannon_entropy(sorted_letter_count)
  print "Min entropy:     ", get_min_entropy(sorted_letter_count)
  print ""
  print "These values differ so much because the probability of the"
  print "most common letter",\
        sorted_letters[-1][0], "(p = " + str(100.0*sorted_letters[-1][1]/total_count) + " %)",\
        "is very high."
  print "This leads to a low Min entropy."
  print ""
  print ""
  print "Task b)"
  print ""
  print "Approach: Minimize the difference between Shannon and Min "
  print "entropy while keeping the Shannon entropy as high as possible"
  print ""
  print "One way to achieve this is to ignore the first n most likely"
  print "characters of the source."
  print ""
  print "n\tShannon\t\tMin\t\tDifference"

  for i in range(1, 16):
    shannon_entropy = get_shannon_entropy(sorted_letter_count[:-i])
    min_entropy = get_min_entropy(sorted_letter_count[:-i])
    diff =  shannon_entropy - min_entropy
    print i, "\t", shannon_entropy, "\t", min_entropy, "\t", diff

  print ""
  print "We only tested differences for removing the first 15 most"
  print "likely characters. The difference would converge to zero"
  print "if one increased the number of ignored characters but this"
  print "would of course reduce the Shannon entropy as well."



compute_entropies("english.txt")
print ""
print ""
print ""
compute_entropies("german.txt")
print ""
print ""
print ""
print "Task c)"
print ""
print "Observations: "
print " -The entropies for the German text are a bit higher than for"
print "  the English text, i.e. the characters in the German text are"
print "  more equally distributed."
print " -Consequently, the entropy differences for German are"
print "  somewhat smaller. Therefore one needs to remove less"
print "  characters to make the entropies converge."

















