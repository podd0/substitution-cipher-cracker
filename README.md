# substitution-cipher-cracker
An all purpose substitution cipher cracker, which is aimed at solving the problem
for any language and for any alphabet.

This is aimed at CTFs, as it's a recurring problem.

# Usage
This requires a list of words of the target language in a text file, one word per line
```
>>> from cracker import monoalphabetic
>>> plaintext = monoalphabetic("dict.txt", ciphertext, flag_format="FLAG")
```
It also accepts a tolerance, which is the number of words of the plaintext that are not
in the dictionary.

It can also be given a partial key, which the user can guess to speed up the execution

# Algorithm 
This is just a backtracking algorithm, which builds a key by doing steps
as small as possible, by choosing a word in the ciphertext and extending
the key to fully translate that word to a word in the dictionary. 

I'm sure it can be optimized (maybe with frequency of letters) as thrashing occurs often if the 
partial guessed key is short
