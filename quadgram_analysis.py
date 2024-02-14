from math import log10

class QuadgramAnalysis(object):
    # REFERENCE: This class is derived from reference 3 in the readme.txt.

    def __init__(self,frequency_definition_file,separator=' '):

        # I construct a temporary "database" of quadgrams and how often 
        # they occur in English.
        self.quadgram_occurances = {}
        for line in open(frequency_definition_file):
            quadgram, count = line.split(separator) 
            self.quadgram_occurances[quadgram] = int(count)

        # To perform the necessary scoring, I need to have some basic 
        # information about the quadgrams.
        self.L = len(quadgram)
        self.N = sum(self.quadgram_occurances.values())
        
        # For each of the quadgrams identified in the file, we want to 
        # calculate a base score. For any that don't occur frequently enough, 
        # we calculate a default floor value.
        for key in self.quadgram_occurances.keys():
            self.quadgram_occurances[key] = log10(float(self.quadgram_occurances[key])/self.N)
        self.floor = log10(0.01/self.N)

    def calculate_score(self,text):
        ''' compute the score of text '''
        score = 0
        ngrams = self.quadgram_occurances.__getitem__
        for i in range(len(text)-self.L+1):
            if text[i:i+self.L] in self.quadgram_occurances: score += ngrams(text[i:i+self.L])
            else: score += self.floor          
        return score