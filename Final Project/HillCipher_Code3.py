"""
Implementation of Hill Cipher!
Important notation:
K = Matrix which is our 'Secret Key'
P = Vector of plaintext (that has been mapped to numbers)
C = Vector of Ciphered text (in numbers)
C = E(K,P) = K*P (mod X) -- X is length of alphabet used
P = D(K,C) = inv(K)*C (mod X)  -- X is length of alphabet used
Programmed by Ivan Ocon
*  2020-11-25
"""
from movie import *
import numpy as np
from egcd import egcd  # pip install egcd

alphabet = 'abcdefghijklmnopqrstuvwxyz '

letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))


def matrix_mod_inv(matrix, modulus):
    """We find the matrix modulus inverse by
    Step 1) Find determinant
    Step 2) Find determinant value in a specific modulus (usually length of alphabet)
    Step 3) Take that det_inv times the det*inverted matrix (this will then be the adjoint) in mod 26"""

    det = int(np.round(np.linalg.det(matrix)))  # Step 1)
    det_inv = egcd(det, modulus)[1] % modulus  # Step 2)
    matrix_modulus_inv = (det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus)  # Step 3)

    return matrix_modulus_inv


def encrypt(message, K):
    encrypted = ''
    message_in_numbers = []

    #Make message into numbers
    for letter in message:
        message_in_numbers.append(letter_to_index[letter])
    
    #Split into the size of matrix K
    split_P = [message_in_numbers[i : i + int(K.shape[0])] for i in range(0, len(message_in_numbers), int(K.shape[0]))]

    #Iterate through each partial message and encrypt is using K*P (mod 26)
    for P in split_P:
        P = np.transpose(np.asarray(P))[:, np.newaxis]

        while P.shape[0] != K.shape[0]:
            P = np.append(P, letter_to_index[' '])[:, np.newaxis]

        numbers = np.dot(K, P) % len(alphabet)
        n = numbers.shape[0]  # length of encrypted message (in numbers)

        # Map it back to get encrypted text
        for idx in range(n):
            number = int(numbers[idx, 0])
            encrypted += index_to_letter[number]

    return encrypted


def decrypt(cipher, Kinv):
    decrypted = ''
    cipher_in_numbers = []

    #Make ciphered text into numbers
    for letter in cipher:
        cipher_in_numbers.append(letter_to_index[letter])

    #Split it into the size of matrix inv(K) so we can do matrix multiplication.
    split_C = [cipher_in_numbers[i : i + int(Kinv.shape[0])] for i in range(0, len(cipher_in_numbers), int(Kinv.shape[0]))]

    #Iterate through each partial text and decrypt using inv(K)*C (mod 26)
    for C in split_C:
        C = np.transpose(np.asarray(C))[:, np.newaxis]
        numbers = np.dot(Kinv, C) % len(alphabet)
        n = numbers.shape[0]

        #Map back numbers to decrypted text
        for idx in range(n):
            number = int(numbers[idx, 0])
            decrypted += index_to_letter[number]

    return decrypted


def main():

    K = np.matrix([[3,10,20],[20,19,17], [23,78,17]]) # for length of alphabet = 27

    Kinv = matrix_mod_inv(K, len(alphabet))
    
    print("Welcome to the movie machine")
    
    myKey = 'http://www.omdbapi.com/?i=tt3896198&apikey=841ba8d4'    
    
    movie = input("Please enter a movie\n")
    
    print("\nOriginal movie:" + movie)
    
    encrypted_msg = encrypt(movie, K)
    
    print("Encrypted movie:" + encrypted_msg)
    
    decrypted_msg = decrypt(encrypted_msg, Kinv)
    
    print("Decrypted movie: " + decrypted_msg)
    
    res = getMovie(myKey, movie)
    
    print("\nAfter a security process here is your most recent movie requested: \n")
    print('Movie:',res['Search'][1]['Title'])
    print('Year:',res['Search'][1]['Year'])
    print('Type:',res['Search'][1]['Type'])


main()