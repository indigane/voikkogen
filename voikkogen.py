#!/usr/bin/env python
# -*- coding: utf-8 -*-

import voikkoinfl
import random
import xml.dom.minidom
import sys

wordlist_xml = 'kotus-sanalista_v1_edited.xml'
wordlist_xml_word_count = 44367

word_classes_subst = voikkoinfl.readInflectionTypes('corevoikko/data/subst.aff')
word_classes_verb = voikkoinfl.readInflectionTypes('corevoikko/data/verb.aff')


try:
  word_count = int(sys.argv[1])
except (IndexError, ValueError):
  word_count = 3


def get_random_inflection(word, type='subst', kotus_class=None, gradclass='-'):
  wordlist = []

  if type == 'verb':
    word_classes = word_classes_verb
  else:
    word_classes = word_classes_subst

  for word_class in word_classes:
    if kotus_class not in word_class.kotusClasses:
      continue
    if len(word_class.joukahainenClasses) == 0:
      continue
    infclass_main = word_class.joukahainenClasses[0]
    inflected_words = voikkoinfl.inflectWordWithType(word, word_class, infclass_main, gradclass or '-')
    if inflected_words == []:
      continue

    for inflected_word in inflected_words:
      wordlist.append(inflected_word.inflectedWord)

  try:
    return random.choice(wordlist)
  except:
    return word


def get_random_word():
  target_index = random.randint(0, wordlist_xml_word_count - 1)
  with open(wordlist_xml, 'r') as fp:
    for index, line in enumerate(fp):
      if index == target_index:
        word = xml.dom.minidom.parseString(line).documentElement.firstChild.firstChild.nodeValue
        try:
          inflection = xml.dom.minidom.parseString(line).documentElement.firstChild.nextSibling.firstChild.firstChild.nodeValue
        except AttributeError:
          inflection = None
        try:
          gradclass = xml.dom.minidom.parseString(line).documentElement.firstChild.nextSibling.firstChild.nextSibling.firstChild.nodeValue
        except AttributeError:
          gradclass = None
        return word, inflection, gradclass


def get_random_inflected_word():
  word, inflection, gradclass = get_random_word()

  if inflection and int(inflection) > 51:
    word_type = 'verb'
  else:
    word_type = 'subst'

  if gradclass in ['A','B','C','E','F','G','H','I','J','K','M'] and any(part in word for part in ['yky', 'uku', 'nk', 'rt', 'lt', 'nt', 'mp', 'kk', 'pp', 'tt']):
    gradclass = 'av1'
  elif gradclass in ['A','B','C','E','F','G','H','I','J','K'] and any(part in word for part in ['mm', 'nn', 'll', 'rr']):
    gradclass = 'av2'
  elif gradclass in ['A','B','C','E','F','G','H','I','J','K','M'] and any(part in word[2:] for part in ['t', 'p']):
    gradclass = 'av1'
  elif gradclass in ['A','B','C','E','F','G','H','I','J','K'] and any(part in word[1:] for part in ['g', 'b', 'd', 'v', 'k', 't', 'p']):
    gradclass = 'av2'
  elif gradclass in ['A','B','C','E','F','G','H','I','J','K','M']:
    gradclass = 'av1'
  elif gradclass in ['A','B','C','E','F','G','H','I','J','K']:
    gradclass = 'av2'
  elif gradclass in ['L',] and 'k' in word[2:]:
    gradclass = 'av3'
  elif gradclass in ['L',] and 'j' in word[2:]:
    gradclass = 'av4'
  elif gradclass in ['L',]:
    gradclass = 'av3'
  elif gradclass in ['D',] and 'k' in word[2:]:
    gradclass = 'av5'
  elif gradclass in ['D',] and 'k' not in word[2:]:
    gradclass = 'av6'
  elif gradclass in ['D',]:
    gradclass = 'av5'
  else:
    gradclass = '-'

  word = get_random_inflection(word, word_type, inflection, gradclass)
  return word


generated_str = ''
try:
  target_count = int(sys.argv[1])
except (IndexError, ValueError):
  target_count = 3

for i in range(target_count):
  generated_str += get_random_inflected_word().capitalize()


print(generated_str)
