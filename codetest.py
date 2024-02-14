import argparse
import random
import enchant
from pycipher import SimpleSubstitution
from quadgram_analysis import QuadgramAnalysis


def retrieve_commandline_arguments():
    # For the program to work, I need three supporting files:
    #  1) the file containing the ciphertext;
    #  2) a list of quadgrams and their frequencies for score calculation; and
    #  3) a word list or dictionary to parse the plaintext message once decrypted.
    # This function accepts those arguments from the commandline, if the user chooses
    # to specify them. It also defines default values for each of those options, 
    # so that the program will remain simple to run.

    program_description = "A simple program to crack monoalphabetic ciphers.\nWritten to fulfill requirements for DSU INFA 723."
    parser = argparse.ArgumentParser(description=program_description)
    parser.add_argument("-c", "--ciphertext", default="./cipher.txt")
    parser.add_argument("-f", "--frequency", default="./english_quadgrams.txt")
    parser.add_argument("-w", "--wordlist", default="./pwl.txt")

    try:
        arguments = parser.parse_args()
    except SystemExit:
        exit()
    
    return arguments


def prepare_ciphertext_for_analysis(original_text):
    # The analysis is significantly more difficult to perform when the 
    # ciphertext contains spaces and punctuation. This function removes
    # those items and standardizes the text into all uppercase characters.

    formatted_text = ""

    for character in original_text:
        if character.isalpha():
            formatted_text += character
    
    formatted_text = formatted_text.upper()
    
    return formatted_text


def parse_plaintext_message(key, ciphertext, dictionary):
    # After the decryption key has been uncovered, the individual words in the message
    # are part of one large string. This function uses a dictionary to recognize each
    # word in the message and adds appropriate spacing.

    plaintext = SimpleSubstitution(key).decipher(ciphertext)
    plaintext_length = len(plaintext)
    message = ""

    forward_position = 0
    while forward_position < plaintext_length:
        for backward_position in range(plaintext_length+1, forward_position, -1):
            if dictionary.check(plaintext[forward_position:backward_position]):
                message = message + " " + plaintext[forward_position:backward_position]
                if plaintext[forward_position:backward_position] == "NSA":
                    message = message + "?"
                forward_position = backward_position
                break
    message = message + "."

    return message



if __name__ == "__main__":
    # This function is the main function of the program and provides much of the 
    # analysis functionality. As an overview, it first initializes the quadgram analysis
    # object for creating scores.
    print("\n[*] Beginning ciphertext analysis. Please stand by...")

    # To start, I retrieve the argument default values, or user-specified values, if any.
    args = retrieve_commandline_arguments()

    # Through previous analysis, I know that the best score that can be reached is -431.1.
    # So, I will stop analysis once that score is reached for efficiency purposes.
    target_score = -432

    # To calculate scores efficiently and quickly, it is necessary to define a class to 
    # handle the quadgram score calculation. This score provides a means to determine 
    # which key is the correct one for decrypting the ciphertext.
    fitness_calculation = QuadgramAnalysis(args.frequency)


    ciphertext_file = open(args.ciphertext, "+r")
    initial_ciphertext=ciphertext_file.read()
    formatted_ciphertext = prepare_ciphertext_for_analysis(initial_ciphertext)

    # REFERENCE: This portion is derived from reference 2 in the readme.txt
    current_key = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    current_score = -100000000

    parentkey = current_key.copy()
    parentscore = current_score
    # keep going until we are killed by the user
    i = 0
    while target_score > parentscore:
        i = i+1
        random.shuffle(parentkey)
        deciphered = SimpleSubstitution(parentkey).decipher(formatted_ciphertext)
        parentscore = fitness_calculation.score(deciphered)
        count = 0
        while count < 1000:
            a = random.randint(0, 25)
            b = random.randint(0, 25)
            child = parentkey[:]
            # swap two characters in the child
            child[a],child[b] = child[b],child[a]
            deciphered = SimpleSubstitution(child).decipher(formatted_ciphertext)
            score = fitness_calculation.score(deciphered)
            # if the child was better, replace the parent with it
            if score > parentscore:
                parentscore = score
                parentkey = child[:]
                count = 0
            count = count+1
        #
        if parentscore > current_score:
            current_score = parentscore
            current_key = parentkey[:]
            print(f"    [+] Hill climbing algorithm determined a better score on try {i}: {current_score}")

    print("[*] Optimal score achieved. Formatting plaintext message...")

    # With the decryption key determined, I can format the plaintext message to be readable.
    final_plaintext = parse_plaintext_message(current_key, formatted_ciphertext, enchant.PyPWL(args.wordlist))
    print(f"\nThe decoded plaintext is: {final_plaintext}")
    print("\tDecryption key: " + "".join(current_key) + "\n")