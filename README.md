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
This is just a backtracking algorithm, which builds a key incrementally.
At each layer of the backtracking tree, we choose `tolerance_max+1` words in the ciphertext to turn 
into words from the dictionary. The way the words to substitute are chosen is "greatest length, least number of characters not in the
partial key".


I'm sure it can be optimized (maybe with frequency of letters) as thrashing occurs often if the 
partial guessed key is short
