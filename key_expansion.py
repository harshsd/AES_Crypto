from BitVector import *

def g(word,S_table,round_constant): #returns the g funtion for a word
    assert word<(2**32)
    q1 = 2**24
    q2 = 2**16
    q3 = 2**8
    a = int(word/q1)
    word = (word%q1) * q3
    word = word + a  #Finished byte roation

    byte1 = int(word/q1)
    word = word%(q1)
    byte2 = int(word/q2)
    word = word % (q2)
    byte3 = int(word / (q3))
    byte4 = word % (q3)

    word = S_table[byte1]*q1 + S_table[byte2]*q2 + S_table[byte3]*q3 + S_table[byte4]

    return word ^ round_constant

def expand_key(key,num_rounds,S_table):
    #key is 128 bit. Restric num_rounds to at max 3

    final_keys = list(key)
    #Now we keep adding 4 words to this list per round required
    round_const = 1
    q5 = 2**25
    for i in range(num_rounds):
        #new refered to as w4,w5,w6,w7
        w4 = final_keys[4*i] ^ g(final_keys[4*i+3],S_table,round_const*q5)
        round_const = 2*round_const
        w5 = w4 ^ final_keys[4*i+1]
        w6 = w5 ^ final_keys[4*i+2]
        w7 = w6 ^ final_keys[4*i+3]
        final_keys.append(w4)
        final_keys.append(w5)
        final_keys.append(w6)
        final_keys.append(w7)
    return final_keys
