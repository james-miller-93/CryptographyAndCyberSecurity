#Padding oracle attack in python version 2.7.10 

from Crypto.Cipher import AES
import binascii
import sys

#import Crypto.Cipher.AES



#Simple example of how to encrypt in python
tkey = 'sixteen byte key'
ivd = '1234567812345678'
obj1 = AES.new(tkey, AES.MODE_CBC, ivd)
message = '11121314151617181112131415161718111213141516171811121314151617181112131415161718111213141516171811121314151617181112131415161711'.decode('hex')
ciphertext = obj1.encrypt(message)
print "ciphertext is:"
print " ".join(hex(ord(n)) for n in ciphertext)


#Check the padding of plaintext
def check_enc(text):
    nl = len(text)
    val = int(binascii.hexlify(text[-1]), 16)
    if val == 0 or val > 16:
        return False

    for i in range(1,val+1):
        if (int(binascii.hexlify(text[nl-i]), 16) != val):
            return False
    return True

#Padding Oracle
def PadOracle(ciphertext):
    if len(ciphertext) % 16 != 0:
        return False
    
    tkey2 = 'sixteen byte key'

    ivd2 = ciphertext[:AES.block_size]
    obj2 = AES.new(tkey2, AES.MODE_CBC, ivd2)
    ptext = obj2.decrypt(ciphertext[AES.block_size:])

    return check_enc(ptext)

# This is sample code written to decrypt only the last byte of the ciphertext
# this function served as an example for the next function implementation
def decryptLastByte(ciphertext):

    for guess in range(256):                # all possible values for the last byte
        modifiedCiphertext = ciphertext[:-17]+ chr(1^int(binascii.hexlify(ciphertext[-17]), 16)^guess) + ciphertext[-16:] 
        #print "modified ciphertext:"
        #print " ".join(hex(ord(n)) for n in modifiedCiphertext)
        if PadOracle(modifiedCiphertext):
            print("Correct guess: ", guess)
            return 1
    return 0

# this function implements the padding oracle attack to decrypt the last k bytes of the input ciphertext
# the function returns the last k bytes of the plaintext
def decryptLastkBytes(ciphertext,k):

    print "\n\n"
    decryptedMessage = []           #   contains the decrypted paintext bytes in reverse order
    for index in range(1,k+1):      #   decrypt the index^th byte of the ciphertext from the end of the array
        for guess in range(256):
            l = list(ciphertext)    #   converted string object to a list since strings aren't mutable
            l[-16-index] = chr(index^int(binascii.hexlify(l[-16-index]), 16)^guess)
            for i in range(1,index):
                l[-16-i] = chr(index^int(binascii.hexlify(l[-16-i]), 16)^decryptedMessage[i-1])
            modifiedCiphertext = "".join(l)
            if PadOracle(modifiedCiphertext):
                decryptedMessage.append(guess)
                break

    return decryptedMessage[::-1]


print decryptLastkBytes(ciphertext,16)

