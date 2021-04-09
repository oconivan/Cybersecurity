from movie import *
import numpy as np

# Python3 code to implement Hill Cipher 

# Generate key matrix  
keyMatrix = [[0] * 3 for i in range(3)] 
  
# Generate vector for the message 
messageVector = [[0] for i in range(3)] 
  
# Generate vector for the cipher 
cipherMatrix = [[0] for i in range(3)]

# Generate vector for the plaintext
plainMatrix = [[0] for i in range(3)] 
  
# Following function generates the 
# key matrix for the key string 
def getKeyMatrix(key): 
    k = 0
    for i in range(3): 
        for j in range(3): 
            keyMatrix[i][j] = ord(key[k]) % 65
            #print(keyMatrix[i][j],key[k])
            k += 1
    #print("Key matrix:")
    #print(keyMatrix)
    #print(type(keyMatrix))
    return keyMatrix
    
  
# Following function encrypts the message 
def encrypt(messageVector): 
    for i in range(3): 
        for j in range(1): 
            cipherMatrix[i][j] = 0
            for x in range(3): 
                cipherMatrix[i][j] += (keyMatrix[i][x] * 
                                       messageVector[x][j]) 
            cipherMatrix[i][j] = cipherMatrix[i][j] % 26
            
    return cipherMatrix

# Following function decrypts the message
def decrypt(messageVector): 
    for i in range(3): 
        for j in range(1): 
            plainMatrix[i][j] = 0
            for x in range(3): 
                plainMatrix[i][j] += (keyMatrix[i][x] * 
                                       messageVector[x][j]) 
            plainMatrix[i][j] = plainMatrix[i][j] % 26
            
    return plainMatrix
 
# This function pass plaintext and key matrix as arguments
def HillCipher(message, key): 
  
    # Get key matrix from the key string 
    getKeyMatrix(key) 
  
    # Generate vector for the message 
    for i in range(3): 
        messageVector[i][0] = ord(message[i]) % 65
        #print(message[i],messageVector[i][0])
    # Following function generates 
    # the encrypted vector 
    encrypt(messageVector) 
  
    # Generate the encrypted text  
    # from the encrypted vector 
    CipherText = [] 
    for i in range(3): 
        CipherText.append(chr(cipherMatrix[i][0] + 65)) 
  
    # Finally print the ciphertext 
    #print("Ciphertext: ", "".join(CipherText))
    return CipherText

# This function pass ciphertext and inverse key as arguments
def decryptHillCipher(message, key): 
  
    # Get key matrix from the key string 
    #getKeyMatrix(key) 
    
    # Generate vector for the message 
    for i in range(3): 
        messageVector[i][0] = ord(message[i]) % 65
        #print(message[i],messageVector[i][0])
    
    #Multiply messageVector by key
    key = np.array(key)
    vector = key.dot(messageVector) % 26
    #print(vector)
    #vector =[np.round(i) for i in vector]
    #print(vector)
    
    # Following function generates 
    # the encrypted vector 
    decrypt(vector) 
    
    # Vector needs to be changed to letters
    # Generate the encrypted text  
    # from the encrypted vector 
    PlainText = [] 
    for i in range(3): 
        PlainText.append(chr(vector[i] + 65)) 
  
    # Finally print the ciphertext 
    #print("Plaintext: ", "".join(PlainText))
    return PlainText

# get minor matrix
def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

# calculate minor matrix
def calcMinorMatrix(N, matrix):
    for i in range(N):
        for j in range(N):
            minor_matrix = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(N):
            minor_matrix[i][j] = round(np.linalg.det(np.array(getMatrixMinor(matrix, i, j))))
    return minor_matrix

# find cofactors
def findCofactors(N, minor_matrix):
    # generate checkerboard of negatives and positives
    for i in range(N):
        for j in range(N):
            chk_matrix = [[1] * N for i in range(N)]
    for i in range(N):
        for j in range(N):
            if (i % 2 == 0) and (j % 2 != 0):
                minor_matrix[i][j] *= -1
            elif (i % 2 != 0) and (j % 2 == 0):
                minor_matrix[i][j] *= -1
    return minor_matrix

# findAdjucateMatrix
def findAdjugateMatrix(cofactor_matrix):
    np_cofactors = np.array(cofactor_matrix)
    np_adjugate = np.transpose(np_cofactors)
    return np_adjugate.tolist()

# calculate inverse
def calculateInverse(adj_matrix, determinant):
    np_adj = np.array(adj_matrix)
    np_inv = (determinant * np_adj) % 26
    return np_inv.tolist()

# find the multiplicative inverse
def find_multiplicative_inverse(determinant):
    multiplicative_inverse = -1
    for i in range(26):
        inverse = determinant * i
        if inverse % 26 == 1:
            multiplicative_inverse = i
            break
    return multiplicative_inverse

# separate into groups on N
def sep(string,n):
    #string = string.replace(" ", "")
    msg = [string[i:i+n] for i in range(0, len(string), n)]
    
    if len(msg[-1]) % n:
        msg[-1] = msg[-1] + ((n - len(msg[-1])) * "*")
    return msg
  
# Driver Code 
def main(): 
  
    print("Welcome to the movie machine")
    
    myKey = 'http://www.omdbapi.com/?i=tt3896198&apikey=841ba8d4'
    
    movie_in = input("Please enter a movie\n")
    movie = movie_in.upper().replace(" ", "[")
    
    #print("\nThis is the movie encrypted from plaintext to ciphertext\n")
    
    # Get the message to  
    # be encrypted 
    message = list(movie)
    #print(message)
    message = sep(movie, 3)
    #print(message)
    
    # Get the key 
    key = "RRFVSVCCT" #key for mod 27
    
    #Convert the key from string to matrix
    A = np.array(getKeyMatrix(key))
    N = 3
    
    #Get the key inverse
    det_A = np.linalg.det(A)
    mult_inv = find_multiplicative_inverse(det_A)
    A = A.tolist()
    mA = calcMinorMatrix(N, A)
    cA = findCofactors(N, mA)
    adj_A = findAdjugateMatrix(cA)
    inverse_key = calculateInverse(adj_A, mult_inv)
    #print(adj_A)
    #print(calculateInverse(adj_A, mult_inv))
    #print("This is the inverse key")
    #print(inverse_key)
    
    #Initialize arrays
    Cipher = []
    Plain = []
    
    # Encrypt the movie
    if message != -1:
        for grp in message:
            #print(grp)
            Cipher.append(HillCipher(grp, key))
            Plain.append(decryptHillCipher(Cipher[-1], inverse_key))
        print("This is the cipher text:", Cipher,"\nThis is the Plain text:", Plain)
        
    res = getMovie(myKey, movie_in)
    
    print("\n")
    print("After a security process here is your most recent movie requested: \n")
    print('Movie:',res['Search'][1]['Title'])
    print('Year:',res['Search'][1]['Year'])
    print('Type:',res['Search'][1]['Type'])
    
if __name__ == "__main__": 
    main()
