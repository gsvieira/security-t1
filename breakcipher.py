import collections
import string
#Usa IC pra determinar o tamanho da chave
possible_keys = []
def get_key_length(ciphertext):
  #divide a messagem em cosets de tamanho 2 a 20 para calculo de IC
  for i in range(2, 21):
    cipher_list = list(ciphertext)
    sublists = []
    IC_avg = 0.0
    #gera matrix de coset com tamanho entre 2 e 20
    for _ in range(i):
      sublists.append([])
    #separa a string nos cosets removendo o primeiro elemento da lista e adicionando ao sublist
    for elem in cipher_list:
      for j in range(i):
        if cipher_list!=[]:
          char= cipher_list.pop(0)
          (sublists[j]).append(char)
    for p in range(i):
      print(sublists[p])
    #calcula o IC
    for k in range(i):
      N = len(sublists[k])
      freq = collections.Counter(sublists[k])
      freq_sum = 0.0
      for elem in string.ascii_lowercase:
        freq_sum += freq[elem] * (freq[elem]-1)
      IC = freq_sum / (N*(N-1))
    #faz média entre os ICs das substrings
    IC_avg +=IC
    possible_keys.append((i, IC_avg/i))
  possible_keys.sort(key= lambda x: x[1], reverse = True)
  return possible_keys #retorna tamanho da chave com maior chance de ser a certa com o IC correspondente

def get_key(message, possible_keys):

  return 0


f = open("output.txt", "r")
message = f.read()
r = get_key_length(message)
print(r)