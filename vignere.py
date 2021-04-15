
MAX_KEYLENGTH = 6 


# List of frequency that english characters occur in a plaintext
ENGLISH_FREQ_LIST = [0.082, 0.015, 0.028, 0.043, 0.127, 0.022, 0.020, 0.061, 0.070, 0.002, 0.008, 0.040, 0.024, 0.067, 0.075, 0.019, 0.001, 0.060, 0.063, 0.091, 0.028, 0.010, 0.023, 0.001, 0.020, 0.001]

# Read ciphertext from file
with open('/vig.txt', 'r') as file:
    cipherText = file.read().replace('\n', '')


# Find the key length first
def find_key_length():
    key_length = 1

    coincidences = []

    coincidenceCount = 0

    while key_length <= MAX_KEYLENGTH:
        
        i = 0
        while i < (len(cipherText) - key_length): #Pad the letters checked by the key length to avoid out of bounds error

            # Compare each letter in ciphertext with letter when shifted by the key length
            if cipherText[i] == cipherText[i + key_length]:
                coincidenceCount += 1
            i += 1 # Go to next letter in ciphertext

        coincidences.append(coincidenceCount) # Same number of coincidences
        key_length += 1 # Try the next key size

    key_length = (coincidences.index(max(coincidences)) + 1) # Get maximum number of coincidences from list, this is the key length

    print("Key length is most likely: " + str(key_length))
    print()

    return key_length

def frequency_analysis(key_length):

    key = "" # The key resulting from the frequency analysis
    i = 0
    # Start with a new position up to the key length
    while i < key_length:

        letter_counts = [] # List with count of each letter
        cipherTextKeyth = "" # String for ciphertext skipping letters by key length

        j = i
        # Count letters skipping by key length
        while j < (len(cipherText)):
            cipherTextKeyth += cipherText[j] # Add to string each letter counting by the key length
            j += key_length # Go to next keyth letter

        # Count each letter in the string and put it in a list
        k = 1
        while k <= 26:
            letter_counts.append(cipherTextKeyth.count(chr(k + 96)))
            k += 1

        # Create a list of the frequency of each letter
        letter_freq = letter_counts

        letter_freq[:] = [round(count / len(cipherTextKeyth), 3) for count in letter_freq] # Divide letter count by total letters and store in list

        # List of lists of shifted frequencys
        shifted_freq_list = [] 

        # Helper function to shift the english frequncy lists
        def shift(seq, n):
            a = n % len(seq)
            return seq[-a:] + seq[:-a]

        # Create shifted frequency list up to 26
        m = 0
        while m < len(ENGLISH_FREQ_LIST):
            shifted_freq_list.append(shift(ENGLISH_FREQ_LIST, m)) # Shift each list by 0-25
            m += 1
        
        # Helper function to calculate the dot product of two lists
        def dot_product(K, L):
            if len(K) != len(L):
                return 0

            return sum(i[0] * i[1] for i in zip(K, L))
        
        # Dot product of each frequency list of the frequency of this ciphertextkeyth list
        dot_products = []
        for freq in shifted_freq_list:
            dot_products.append(round(dot_product(letter_freq, freq),3 ))


        # Find the largest value from the list of dot products, this is most likely the key for this position
        max_dot_product= (dot_products.index(max(dot_products)) + 1)
        print(max_dot_product, end=" ")

        # Add character to key
        key += chr(max_dot_product + 96) # Convert int to the key character


        i += 1 # Start with next position

    print(key)
    return key


def decryptV(key):

    key_int = [] # key in integer form

    for letter in key:
        key_int.append(ord(letter) - 96) # Convert key to ints for shifting

    cipher_int  = []
    for letter in cipherText:
        cipher_int.append(ord(letter) - 96) # Convert key to ints for shifting


    plaintext = "" # Plaintext to output from decryption

    i = 0
    while i < len(cipher_int): 

        plaintext_char = cipher_int[i] - (key_int[i % len(key_int)]) % 26 + 1 # Decrypt using Vigenere alogorithm
        if(plaintext_char < 0):
            plaintext_char += 26 # Convert negative numbers to positive mod 26
        plaintext_char = chr(plaintext_char + 96) # Convert from int to string
        plaintext += plaintext_char # Add char to the string

        i += 1 # Decrypt the next letter

    print(plaintext)



if __name__ == "__main__":
    key_length = find_key_length()

    key1 = frequency_analysis(key_length)

    key2 = frequency_analysis(5)

    key3 = frequency_analysis(4)

    decryptV(key3)