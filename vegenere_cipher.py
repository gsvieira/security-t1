import string, re, sys
characters = list(string.ascii_lowercase) #+ list(string.digits) + [" "]

map_int_to_char = {}
map_char_to_int = {}

i=0
for char in characters:
  map_int_to_char[i] = char
  map_char_to_int[char] = i
  i+=1

last_char_position = len(map_int_to_char)-1

def cipher(message, key):
  #message = message.replace("\n", " ").lower()
  message = re.sub("[^a-zA-Z]+","", message).lower()
  cipher_message = []
  key_index = 0
  list_key = list(key.strip(" "))
  for character in message:
    if key_index > len(list_key)-1:
      key_index = 0
    key_char = list_key[key_index]
    
    key_char_value = map_char_to_int[key_char]
    message_char_value = map_char_to_int[character]
    new_char_value = message_char_value + key_char_value

    if new_char_value > last_char_position:
      new_char_value = new_char_value - last_char_position - 1
    new_char = map_int_to_char[new_char_value]
    cipher_message.append(new_char)
    key_index+=1
  return "".join(cipher_message)

def decipher(message, key):
  message = re.sub("[^a-zA-Z]+","", message).lower()
  deciphered_message = []
  key_index = 0
  list_key = list(key.strip(" "))
  for character in message:
    if key_index > len(list_key)-1:
      key_index = 0
    key_char = list_key[key_index]

    key_char_value = map_char_to_int[key_char]
    message_char_value = map_char_to_int[character]
    new_char_value = message_char_value - key_char_value

    if new_char_value < 0:
      new_char_value = new_char_value + last_char_position + 1
    new_char = map_int_to_char[new_char_value]
    deciphered_message.append(new_char)
    key_index+=1
  return "".join(deciphered_message)


#inicio do codigo
if len(sys.argv)<=1:
  print("É necessario o nome do arquivo que deseja abrir -> breakcipher.py nomedoarquivo.txt")
  sys.exit()
file = open("input.txt","r")
message = file.read()
file.close()

message_ciphered = cipher(message, sys.argv[1])

f = open("ciphered.txt","w")
f.write(message_ciphered)
f.close()

message_deciphered = decipher(message_ciphered, sys.argv[1])

f = open("deciphered.txt","w")
f.write(message_deciphered)
f.close()