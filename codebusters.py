import math
# PART 0 // THE BUILDING BLOCKS

# array, contains all of the letters of the alphabet
alphabet = [l for l in 'abcdefghijklmnopqrstuvwxyz']

# a dictionary mapping each letter of the alphabet to its index (i.e a: 0, b: 1, c: 2) 
# by using the alphabet array
alphanumeric = {alphabet[i]: i for i in range(26)}

# an inverse of alphanumeric, maps each index to its respective letter
rev_alpha = {n: a for a, n in alphanumeric.items()}

# converts a string into an array of numbers (i.e abc becomes [0, 1, 2])
def str_to_nums(s: str):
    s_arr = list(s)
    i_arr = []
    for b in s_arr:
        if b != ' ':
            i_arr.append(alphanumeric[b])
    return i_arr

# finds all of the space indices in a string; makes it way easier to work with later
def find_spaces(s: str):
    s_arr = list(s)
    spaces = []
    for i in range(len(s_arr)):
        if s_arr[i] == ' ':
            spaces.append(i)
    return spaces

# adds spaces back into a string after it has been processed
def add_spaces(s_arr: list, spaces: list):
    for space in spaces:
        s_arr.insert(space, ' ')
    return ''.join(s_arr)

# multiplicative inverses of all numbers coprime with 26 (used in affine cipher)
inverses = {1: 1, 3: 9, 5: 21, 7: 15, 9: 3, 11: 19, 15: 7, 17: 23, 19: 11, 21: 5, 23: 17, 25: 25}

# PART 1 // CAESAR ENCRYPTION + BRUTE FORCE DECRYPTION

# performs caesar encryption based on the shift (i) and the phrase (s)
def caesar_encrypt(s: str, i: int):
    # converts s into array of indices
    i_arr = str_to_nums(s)
    spaces = find_spaces(s)

    # shifts indices, maps to respective letters, prints final output
    caesar = []
    for r in i_arr:
        if r != ' ':
            caesar.append(rev_alpha[(r + i) % 26])
        else:
            caesar.append(' ')
    print(add_spaces(caesar, spaces))

# decrypts a string encrypted with caesar
# brute forces through all 26 shifts
def caesar_decrypt(s: str):
    for i in range(26):
        caesar_encrypt(i, s)

# PART 2: ATBASH CIPHER ENCRYPTION/DECRYPTION

# because atbash is its own inverse, the same algorithm can be
# used for encrypting and decrypting
def atbash_cipher(s: str):
    # converts s into array of indices
    i_arr = str_to_nums(s)
    spaces = find_spaces(s)

    # encrypts and prints s
    atbash = []
    for r in i_arr:
        if r != ' ':
            atbash.append(rev_alpha[25 - r])
        else:
            atbash.append(' ')
    print(add_spaces(atbash, spaces))

# PART 3: AFFINE CIPHER

# encryption algorithm
def affine_encrypt(s: str, a: int, b: int):
    # converts s into array of indices
    i_arr = str_to_nums(s)
    spaces = find_spaces(s)

    # performs affine cipher based on a, b and s then prints
    affine = []
    for r in i_arr:
        if r != ' ':
            affine.append(rev_alpha[(a * r + b) % 26])
        else:
            affine.append(' ')
    print(add_spaces(affine, spaces))

# decryption algorithm based on encryption key
def affine_decrypt(s: str, a: int, b: int):
    i_arr = str_to_nums(s)
    spaces = str_to_nums(s)

    # finds multiplicative inverse of a
    a = inverses[a]

    # decrypts and prints s
    affine_r = []
    for r in i_arr:
        if r != ' ':
            affine_r.append(rev_alpha[(a * (r - b)) % 26])
        else:
            affine_r.append(' ')
    print(add_spaces(affine_r, spaces))

# PART 4: VIGENERE CIPHER

# encrypts vigenere cipher based on s and key
def vigenere_encrypt(s: str, key: str):
    i_arr = str_to_nums(s)
    ik_arr = str_to_nums(key)
    vigenere = []
    index = 0
    spaces = find_spaces(s)

    # the vigenere cipher is equivalent to (a + b) % 26 given that 
    # a and b are indices of the letters being used
    for r in i_arr:
        if r != ' ':
            vigenere.append(rev_alpha[(r + ik_arr[index % len(key)]) % 26])
            index += 1
        else:
            vigenere.append(' ')
    print(add_spaces(vigenere, spaces))

# PART 5: HILL CIPHER (the annoying one)

# performs the matrix multiplication necessary. 
# ** technically the for loop parameters aren't right BUTTT 
# the key matrix is always square so it has zero effect
def matrix_multiplication(phrase, key):
    l = len(phrase)
    letters = []
    for i in range(l):
        s = 0
        for j in range(l):
            s += key[i][j] * phrase[j]
        s %= 26
        sl = rev_alpha[s]
        letters.append(sl)
    return ''.join(letters)

# performs hill cipher encryption/decryption
def hill_cipher(s, key, mode):
    i_arr = str_to_nums(s)
    spaces = find_spaces(s)

    # pads the string with Zs so that there are no errors with matrix multiplication 
    bin_size = int(math.sqrt(len(key)))
    runoff = len(s) % bin_size
    if runoff != 0:
        for i in range(bin_size - runoff):
            i_arr.append(25)

    # converts key into an array, and then into a 2D array afterwards
    ik_temp = str_to_nums(key)
    ik_arr = []
    if(len(key) == 4):
        ik_arr = [ik_temp[:2] , ik_temp[2:]]
    else:
        ik_arr = [ik_temp[:3], ik_temp[3:6], ik_temp[6:]]
    
    # changes matrix into decryption matrix if in decrypt mode
    if mode == 'd':
        if(decryption_matrix(ik_arr) == False):
            print("could not decrypt")
            return 
        else:
            ikf_arr = decryption_matrix(ik_arr)
    else:
        ikf_arr = ik_arr

    # does all of the matrix multiplication, inserts spaces and concatenates results
    final = []
    for i in range(len(i_arr) // bin_size):
        bin_encrypted = matrix_multiplication(i_arr[(bin_size * i): (bin_size * (i + 1))], ikf_arr)
        final.append(bin_encrypted)
    transitory = list(''.join(final))
    print(add_spaces(transitory, spaces))
    

# finds decryption matrix given encryption matrix by 
# a: finding multiplicative inverse of determinant and 
# b: finding the adjoint matrix
def decryption_matrix(key_matrix):
    # finds inverse determinant of matrix IF matrix is invertible; throws error otherwise
    det = ((key_matrix[1][1] * key_matrix[0][0]) - (key_matrix[0][1] * key_matrix[1][0])) % 26
    if det not in inverses:
        print("decryption matrix could not be found")
        return False
    else:
        det_inv = inverses[det]
       
    # creates adjoint matrix, multiplies by inverse determinant
    af = key_matrix[1][1] * det_inv % 26
    bf = (26 - key_matrix[0][1]) * det_inv % 26
    cf = (26 - key_matrix[1][0]) * det_inv % 26
    df = key_matrix[0][0] * det_inv % 26
    final = [[af, bf], [cf, df]]
    return final

# PART 6: PUTTING IT ALL TOGETHER

# takes in user input, runs the appropriate cipher
def code_bust():
    again = 'y'
    while(again == 'y'):
        print("what cipher are you using?")
        print("     caesar (enter c)")
        print("     atbash (enter at)")
        print("     affine (enter af)")
        print("     vigenere (enter v)")
        print("     hill (enter h)")
        cipher = input()
        s = input("what phrase are you encrypting/decrypting? ")
        if cipher == 'c':
            mode = input("encrypt (e) or decrypt (d)? ")
            if mode == 'e':
                i = int(input("what is the shift? "))
                caesar_encrypt(s, i)
            else: 
                caesar_decrypt(s)
        elif cipher == 'at':
            atbash_cipher(s)
        elif cipher == 'af':
            mode = input("encrypt (e) or decrypt (d)? ")
            a, b = map(int, input("what are the values of a and b? ").split())
            if mode == 'e':
                affine_encrypt(s, a, b)
            else:
                affine_decrypt(s, a, b)
        elif cipher == 'v':
            key = input("what is the encryption key? ")
            vigenere_encrypt(s, key)
        elif cipher == 'h':
            mode = input("encrypt (e) or decrypt (d)? ")
            key = input("what is the encryption key? ")
            hill_cipher(s, key, mode)
        else:
            print("please enter a valid cipher.")
        again = input('would you like to encrypt/decrypt another message (y or n)? ')

# busts the code.
if __name__ == '__main__':
    code_bust()
