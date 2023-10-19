import sys
import numpy as np


input_filename = sys.argv[1]
out_filename = sys.argv[2]
words = sys.argv[3:]

with open(input_filename, 'r') as f:
    lines = f.readlines()


map_index_word = {} ## stores words -> index mapping
map_word_index = {} ## stores index -> words mapping
u = []
for i, line in enumerate(lines[1:]):
    vals = line.split()
    row = [float(vals[i]) for i in range(1, len(vals))]
    word = vals[0]
    map_index_word[word] = i
    map_word_index[i] = word
    u.append(row)

U = np.array(u)
U_mul_Ut = np.dot(U, U.transpose())

v = U.shape[0]
one_indices = [] ## to store those indices of terms which occur in the dictionary
for word in words:
    if word in map_index_word.keys():
        one_indices.append(map_index_word[word])

a = np.array(one_indices)
query_vector = np.zeros((v,1), dtype=int)
query_vector[a] = 1
distance_scores = np.dot(U_mul_Ut, query_vector)


## multiply U * Ut * q
sorted_indices = np.argsort(distance_scores.flatten())
top_k_indices = sorted_indices[:20]
top_k_words = [map_word_index[i] for i in top_k_indices]
print(top_k_words)

with open(out_filename, 'w') as f:
    for word in top_k_words:
        f.write(word +'\n')

   