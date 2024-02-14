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

    # I open the file containing the ciphertext and prepare the ciphertext for analysis.
    ciphertext_file = open(args.ciphertext, "+r")
    initial_ciphertext=ciphertext_file.read()
    formatted_ciphertext = prepare_ciphertext_for_analysis(initial_ciphertext)

    # REFERENCE: The following while loop is derived from reference 2 in the readme.txt
    # As mentioned in readme.txt, I need a starting key and I need a score for comparison.
    current_key = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    current_score = -100000000

    # The goal of the hill climbing algorithm is to find the best possible option 
    # among lots of small variations. However, one weakness of this algorithm is 
    # that it can sometimes get stuck on a local maximum. By randomly "jumping" to 
    # a different key and trying local variations from that key, I can avoid this problem.
    lucky_jump_key = current_key.copy()
    lucky_jump_score = current_score
    attempt = 0
    
    while target_score > lucky_jump_score:
        attempt += 1
        
        # I perform the random jump, attempt to decrypt the text, and score the attempt.
        random.shuffle(lucky_jump_key)
        attempted_decryption = SimpleSubstitution(lucky_jump_key).decipher(formatted_ciphertext)
        lucky_jump_score = fitness_calculation.calculate_score(attempted_decryption)
        local_variant = 0
        
        # From the random jump, I will try a number of different minor variations. 
        # The goal of this is to determine if another key is better suited to the 
        # decryption, i.e. gets the ciphertext closer to recognized English.
        while local_variant < 1000:
            a = random.randint(0, 25)
            b = random.randint(0, 25)
            local_variant_key = lucky_jump_key.copy()
            local_variant_key[a],local_variant_key[b] = local_variant_key[b],local_variant_key[a]
            attempted_decryption = SimpleSubstitution(local_variant_key).decipher(formatted_ciphertext)
            local_variant_score = fitness_calculation.calculate_score(attempted_decryption)

            # If the local variant is better, this can be used as the new local peak to start from. 
            # We continue trying local variations until one is not found better after 1000 attempts. 
            # If we reach 1000 attempts, we can be fairly certain we have the local peak.
            if local_variant_score > lucky_jump_score:
                lucky_jump_score = local_variant_score
                lucky_jump_key = local_variant_key.copy()
                local_variant = 0
            local_variant += 1
        
        # Once we've established a local peak, we track that as the maximum peak. Once we hit the 
        # projected score of -432, we can safely assume that we have the maximum peak, i.e. we have 
        # the correct encryption key.
        if lucky_jump_score > current_score:
            current_score = lucky_jump_score
            current_key = lucky_jump_key.copy()
            print(f"    [+] Hill climbing algorithm determined a better score on attempt #{attempt}: {current_score}")

    print("[*] Optimal score achieved. Formatting plaintext message...")

    # With the decryption key determined, I can format the plaintext message to be readable.
    final_plaintext = parse_plaintext_message(current_key, formatted_ciphertext, enchant.PyPWL(args.wordlist))
    print(f"\nThe decoded plaintext is: {final_plaintext}")
    print("\tDecryption key: " + "".join(current_key) + "\n")