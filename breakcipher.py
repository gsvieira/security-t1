import collections, string, re


#Usa IC pra determinar o tamanho da chave
possible_keys = []
def get_key_length(ciphertext):
  #corrige espaços e outros caracteres não alphanumericos
  ciphertext_treated = re.sub("[^a-zA-Z]+","", ciphertext).lower()
  file = open("intermediario.txt","w")
  file.write(ciphertext_treated)
  #divide a messagem em cosets de tamanho 2 a 10 para calculo de IC Bug chave = 8
  for i in range(2,11):
    cipher_list = list(ciphertext_treated)
    cipher_list_size = len(cipher_list)
    sublists = []
    IC_list = [] #testar media de IC
    IC_sum, IC = 0.0, 0.0
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
    #print(IC_list)
    #faz média entre os ICs das substrings
    possible_keys.append((i, IC_sum/i))#acrecentar '/i'
  possible_keys.sort(key= lambda x: x[1], reverse = True)
  return possible_keys #retorna tamanho da chave com maior chance de ser a certa com o IC correspondente

def get_key(ciphertext):
  possible_keys = get_key_length(ciphertext)
  ciphertext_treated = re.sub("[^a-zA-Z]+","", ciphertext).lower()
  alphabet_size = len(string.ascii_lowercase)
  cipher_list = list(ciphertext_treated)
  cipher_list_size = len(cipher_list)
  english_letter_frequency = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.0015, 0.01974, 0.00074]

  portuguese_letter_frequency = [0.1463, 0.0104, 0.0388, 0.0499, 0.1257, 0.0102, 0.013, 0.0128, 0.0618, 0.004, 0.0002, 0.0278, 0.0474, 0.0505, 0.1073, 0.0252, 0.012, 0.0653, 0.0781, 0.0434, 0.0463, 0.0167, 0.0001, 0.0021, 0.0001, 0.0047]

  sublists = []
  key_result = []
  result = ""
  #possible_keys = get_key_length(message)
  #divide a mensagem em cosets em quantidade igual ao tamanho da chave
  key_size = possible_keys[0][0]
  for _ in range(key_size):
    sublists.append([])
  for j in range(cipher_list_size):
    char = cipher_list.pop(0)
    (sublists[j%key_size]).append(char)
  #faz para cada letra da chave
  for i in range(key_size):
    x_square = []
    #tenta para todo shift possivel da letra
    for j in range(0,(-alphabet_size), -1):
      N = len(sublists[i])
      count = collections.Counter(sublists[i])
      count_list = list(count.items())
      #ajeita lista para ter todos as letras do alfabeto
      for letter in string.ascii_lowercase:
        try:
          [x[0] for x in count_list].index(letter)
        except ValueError:
          count_list.append((letter, 0))
      count_list.sort(key= lambda x: x[0])
      
      f_sum = 0.0
      #print(len(count_list))
      for k in range (alphabet_size):
        freq = count_list[k][1]/N
        f_sum+=((freq-english_letter_frequency[j+k])**2)/(english_letter_frequency[j+k])
      x_square.append((-j ,f_sum))
    x_square.sort(key= lambda x: x[1])
    key_result.append(x_square[0][0])
    result+=string.ascii_lowercase[x_square[0][0]]
  return result


""" list1 = [('a',0)]
for letter in string.ascii_lowercase:
        try:
          [x[0] for x in list1].index(letter)

        except ValueError:
          list1.append((letter, 0))
print(list1) """




"""f = open("ciphered.txt", "w")
for letter in ("abc"):
  for _ in range(7):
    f.write(letter)
f.close"""
#file = open("intermediario.txt", "w")



f = open("desafio2.txt", "r")
message = f.read()
#print(len(message))
r = get_key(message)
print(r)
f.close
#file.close