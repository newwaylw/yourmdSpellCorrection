#! /usr/bin/env python3
import sys,re,math
from collections import Counter
from scipy.spatial import distance
import numpy as np
import pandas as pd

class SpellCorrection:

  def __init__(self, a_file, word_vector_file):
    self.unigram_cnt = Counter()
    self.edit_distance_cnt = Counter()
    self.unigram_count = 0
    self.load_unigram(a_file)
    self.dis_matrix = self.vector_distance(word_vector_file)
    #edit distance penalty if the first letter is different 
    self.initial_penalty_distance = 5
  def levenshtein(self, s1, s2):
    if len(s1) < len(s2):
      return self.levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
      return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
      current_row = [i + 1]
      for j, c2 in enumerate(s2):
        insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
        deletions = current_row[j] + 1       # than s2
        substitutions = previous_row[j] + (c1 != c2)
        current_row.append(min(insertions, deletions, substitutions))
      previous_row = current_row

    return previous_row[-1]


  #return a cosine distance co-matrix on word vectors.
  #word vector trained on symptom.csv using word2vec
  def vector_distance(self, word_vec, metric='cosine'):
    X = np.genfromtxt(word_vec, delimiter=' ', usecols=range(1,128))
    self.y = np.genfromtxt(word_vec, dtype=object, delimiter=' ', usecols=[0]).astype(str)
    dis = distance.cdist(X, X, metric)
    return np.absolute(dis);

  def load_unigram(self, a_file):
    with open(a_file) as f:
      for line in f:
        (word, freq) = re.split('\s+', line.strip())
        self.unigram_cnt[word] = int(freq)
        self.unigram_count += int(freq)

  #get likely spell correction candidates, return 5 candidates by default
  def get_predictions(self, target_word, num=5):
    if len(target_word) ==0:
      return []
    result = list()
    candidate_list = list()
    for w,f in self.unigram_cnt.most_common():
      d = self.levenshtein(target_word, w)

      #it is very unlikely a user will make mistake on the first letter,
      #so apply penalty if this happens.
      if(w[0] != target_word[0]):
        d+=self.initial_penalty_distance

      self.edit_distance_cnt[w] = d

    for w,d in reversed(self.edit_distance_cnt.most_common()):
      candidate_list.append((w,d))

    for w,d in candidate_list[:num]:
      prob = 1.0 if d==0 else (self.unigram_cnt[w]+1) / self.unigram_count
      idx_w = np.where(self.y==w)[0]
      idx_target = np.where(self.y==target_word)[0]
      #we have similarity info. [0-1], smaller the closer.
      distance = 0
      if(len(idx_w) ==1 and len(idx_target)==1):
        #print("w1=", self.y[idx_w], "w2=", self.y[idx_target])
        #print("index of w=",idx_w, " index of target candidate=",idx_target)
        #print(self.dis_matrix.shape)
        distance = self.dis_matrix[idx_w[0]][idx_target[0]]

      print(w,"prob=",prob, " similarity distance=",distance, " edit_distance=", d, " exp=",math.exp(d))
      score = prob/(math.exp(d) * math.exp(distance))
      result.append((w,score))
    return sorted(result, key=lambda x : x[1], reverse=True)


def main():
  sc = SpellCorrection(sys.argv[1], sys.argv[2])
  t_word = sys.argv[3]
  l = sc.get_predictions(t_word)
  print(l)


if __name__ == '__main__':
  main()