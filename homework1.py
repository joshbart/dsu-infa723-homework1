import argparse
import logging


def retrieve_commandline_arguments():
    program_description = "A simple program to crack monoalphabetic ciphers.\nWritten to fulfill requirements for DSU INFA 723."
    parser = argparse.ArgumentParser(description=program_description)
    parser.add_argument("filename")
    try:
        args = parser.parse_args()
    except SystemExit:
        exit()
    return args


def prepare_ciphertext_for_analysis(original_text):
    formatted_text = ""
    for character in original_text:
        if character.isalpha():
            formatted_text += character
    formatted_text.upper()
    return formatted_text


if __name__ == "__main__":
    # Set up logging to print messages to the console
    logging.getLogger().setLevel(logging.INFO)
    
    logging.info(" Opening cipher text file...")
    ciphertext_file = open(retrieve_commandline_arguments().filename, "+r")
    
    logging.info(" Reading contents of cipher text file...")
    ciphertext = ciphertext_file.read()

    logging.info(" Reformatting the ciphertext for analysis...")
    formatted_ciphertext = prepare_ciphertext_for_analysis(ciphertext)


    print(formatted_ciphertext)
    # TODO: (Optional) Perform some sort of frequency analysis to generate a place to start
    # 

