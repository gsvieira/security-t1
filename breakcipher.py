

#Usa Ic pra determinar o tamanho da chave
possible_keys = []
sublists = [0,0]
def get_key_lenght(ciphertext):
  for i in range(2, 21):
    chipher_list = list(ciphertext)
    for j in range (1, i+1):
      sublists [j]= chipher_list.pop(1)

"""use list pop to split the message into multiple substrings"""