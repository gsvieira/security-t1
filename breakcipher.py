import collections, string, re


#Usa IC pra determinar o tamanho da chave
possible_keys = []
def get_key_length(ciphertext):
  #corrige espaços e outros caracteres não alphanumericos
  ciphertext_treated = re.sub("[^a-zA-Z]+","", ciphertext).lower()
  file.write(ciphertext_treated)
  #divide a messagem em cosets de tamanho 2 a 10 para calculo de IC Bug chave = 8
  for i in range(2,11):
    cipher_list = list(ciphertext_treated)
    cipher_list_size = len(cipher_list)
    sublists = []
    IC_list = [] #testar media de IC
    IC_sum, IC = 0.0, 0.0
    print(IC)
    #gera matrix de coset com tamanho entre 2 e 10
    for _ in range(i):
      sublists.append([])
      IC_list.append([])
    #separa a string nos cosets removendo o primeiro elemento da lista e adicionando ao sublist
    for j in range(cipher_list_size):
      char = cipher_list.pop(0)
      (sublists[j%i]).append(char)
    #test
    """ for p in range(i):
      print(sublists[p]) """
    #calcula o IC
    for k in range(i):
      N = len(sublists[k])
      freq = collections.Counter(sublists[k])
      freq_sum = 0.0
      for elem in string.ascii_lowercase:
        freq_sum += freq[elem] * (freq[elem]-1)
      if N==0:
        IC = 0
      else:
        IC = freq_sum / (N*(N-1))
      IC_list[k].append((i, IC))
      IC_sum +=IC
    print(IC_list)
    #faz média entre os ICs das substrings
    possible_keys.append((i, IC_sum/i))#acrecentar '/i'
  possible_keys.sort(key= lambda x: x[1], reverse = True)
  return possible_keys #retorna tamanho da chave com maior chance de ser a certa com o IC correspondente

def get_key(message, possible_keys):

  return 0


"""f = open("ciphered.txt", "w")
for letter in ("abc"):
  for _ in range(7):
    f.write(letter)
f.close"""
file = open("intermediario.txt", "w")



f = open("desafio1.txt", "r")
message = f.read()
print(len(message))
r = get_key_length(message)
f.close
file.close
print(r)
