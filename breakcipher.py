import collections, string, re, sys


#Usa IC pra determinar o tamanho da chave
def get_key_length(ciphertext):
  possible_keys = []
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

def get_key(ciphertext, key_lenght=0):
  if not(int(key_lenght)):
    possible_keys = get_key_length(ciphertext)
  else:
    possible_keys = [[int(key_lenght)]]
  ciphertext_treated = re.sub("[^a-zA-Z]+","", ciphertext).lower()
  alphabet_size = len(string.ascii_lowercase)
  cipher_list = list(ciphertext_treated)
  cipher_list_size = len(cipher_list)
  english_letter_frequency = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.0015, 0.01974, 0.00074]

  portuguese_letter_frequency = [0.1463, 0.0104, 0.0388, 0.0499, 0.1257, 0.0102, 0.013, 0.0128, 0.0618, 0.004, 0.0002, 0.0278, 0.0474, 0.0505, 0.1073, 0.0252, 0.012, 0.0653, 0.0781, 0.0434, 0.0463, 0.0167, 0.0001, 0.0021, 0.0001, 0.0047]

  sublists = []
  key_result_eng = []
  key_result_pt = []
  result_eng = ""
  result_pt = ""
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
    x_square_eng = []
    x_square_pt = []
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
      
      f_sum_eng = 0.0
      f_sum_pt = 0.0
      #print(len(count_list))
      for k in range (alphabet_size):
        freq = count_list[k][1]/N
        f_sum_eng+=((freq-english_letter_frequency[j+k])**2)/(english_letter_frequency[j+k])
        f_sum_pt+=((freq-portuguese_letter_frequency[j+k])**2)/(portuguese_letter_frequency[j+k])
      x_square_eng.append((-j ,f_sum_eng))
      x_square_pt.append((-j ,f_sum_pt))
    x_square_eng.sort(key= lambda x: x[1])
    x_square_pt.sort(key= lambda x: x[1])
    if verbose:
      for l in range(1,3):
        print(x_square_eng[l])
        print(x_square_pt[l])
    key_result_eng.append(x_square_eng[0][0])
    key_result_pt.append(x_square_pt[0][0])

    result_eng+=string.ascii_lowercase[x_square_eng[0][0]]
    result_pt+=string.ascii_lowercase[x_square_pt[0][0]]
  return (result_eng, result_pt)

#inicio do programa
verbose = False
if len(sys.argv)<=1:
  print("É necessario o nome do arquivo que deseja abrir -> breakcipher.py nomedoarquivo.txt")
  sys.exit()
f = open(sys.argv[1], "r")
message = f.read()
if len(sys.argv)==3:
  if sys.argv[2]=="-v":
    r = get_key(message)
    verbose = True
  else:
    r = get_key(message, sys.argv[2])
elif len(sys.argv)>3:
  r = get_key(message, sys.argv[2])
  if "-v"in sys.argv:
    verbose = True
else:
  r = get_key(message)
print("Possivel chave em ingles: {}\nPossivel chave em portugues: {}".format(r[0],r[1]))
f.close