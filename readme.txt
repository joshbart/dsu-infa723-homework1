DSU INFA 723 HOMEWORK 1
SUBMITTED BY JOSHUA BARTHOLOMEW

Plaintext: "WANT TO KNOW WHAT IT TAKES TO WORK AT NSA? CHECK BACK EACH MONDAY IN MAY AS WE EXPLORE CAREERS ESSENTIAL TO PROTECTING OUR NATION."



HOW TO COMPILE
==============

First, start and activate a virtual environment. For Windows, the commands are:
> python -m venv .venv
> .venv\Scripts\Activate

On Linux, the commands are:
$ python3 -m venv .venv
$ source .venv/bin/activate

Once activated, install dependencies (same command for Windows and Linux):
$ pip3 install -r requirements.txt




HOW TO RUN
==========

The command is the same on Linux or Windows. The program has default values specified already and does not require additional input.
$ python3 homework1.py

Optionally, you may specify certain flags.
$ python3 homework1.py -c <ciphertext_file> -f <frequency_reference_file> -w <wordlist_file>

Example: $ python3 homework1.py -c cipher.txt -f english_quadgrams.txt -w pwl.txt




EXPECTED OUTPUT
===============

[*] Beginning ciphertext analysis. Please stand by...
    [+] Hill climbing algorithm determined a better score on try 1: -504.96440456886575
    [+] Hill climbing algorithm determined a better score on try 2: -498.6070422054415
    [+] Hill climbing algorithm determined a better score on try 4: -483.7011188359655
    [+] Hill climbing algorithm determined a better score on try 5: -460.68693109718447
    [+] Hill climbing algorithm determined a better score on try 17: -432.5413722871861
    [+] Hill climbing algorithm determined a better score on try 28: -431.10849018770915
[*] Optimal score achieved. Formatting plaintext message...

The decoded plaintext is:  WANT TO KNOW WHAT IT TAKES TO WORK AT NSA? CHECK BACK EACH MONDAY IN MAY AS WE EXPLORE CAREERS ESSENTIAL TO PROTECTING OUR NATION.
        Decryption key: PHQGIYMEAULNOFDXJKRCVBTZWS

NOTE: the final decryption key may not be exactly the same. This is due to some of the trailing letters being unused in the message. This 
means the effectiveness of slightly varied keys is identical.




ADDITIONAL DESCRIPTIONS
=======================

To complete this assignment, I conducted some research into ways to use hill climbing algorithms to analyze and break substitution ciphers. 
According to Wildon [1], there are three things needed to solve a substitution cipher using hill climbing: 1) an initial value for the key; 
2) a way to step through other keys for comparison; and 3) a scoring method for comparing keys. Wildon discussed some of the various scoring 
methods using monograms, bigrams, and a full word list. However, he referenced Lyons [3] as the best approach to cracking these types of 
ciphers. Lyons suggests that the best performance is reached by using quadgrams. Any increase in the number of characters reviewed at one time, 
according to Lyons, does not increase the efficiency.

References:
[1] M. Wildon, "Hill climbing on substitution ciphers," Wildon's Weblog, May 2018. Accessed: Jan. 29, 2024. [Online]. Available: https://wildonblog.wordpress.com/2018/05/22/hill-climbing-on-substitution-ciphers/
[2] J. Lyons, "Cryptanalysis of the Simple Substitution Cipher," Practical Cryptography. Accessed: Jan. 29, 2024. [Online]. Available: http://practicalcryptography.com/cryptanalysis/stochastic-searching/cryptanalysis-simple-substitution-cipher/
[3] J. Lyons, "Quadgram Statistics as a Fitness Measure," Practical Cryptography. Accessed: Jan. 29, 2024. [Online]. Available: http://practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/