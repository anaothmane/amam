##from Bio.Align.Applications import MuscleCommandline
##help(MuscleCommandline)
##
##from Bio.Align.Applications import MuscleCommandline
##cline = MuscleCommandline(input="opuntia.fasta", out="opuntia.txt")
##print(cline)
##muscle -in opuntia.fasta -out opuntia.txt
##

import Sentiment

text = """bad. bad. bad"""

splitter = Sentiment.Splitter()
postagger = Sentiment.POSTagger()
dicttagger = Sentiment.DictionaryTagger([ 'dicts/positive.yml', 'dicts/negative.yml', 
                                'dicts/inc.yml', 'dicts/dec.yml', 'dicts/inv.yml'])

splitted_sentences = splitter.split(text)
# pprint(splitted_sentences)

pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
# pprint(pos_tagged_sentences)

dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
# pprint(dict_tagged_sentences)

print("analyzing sentiment...")
score = Sentiment.sentiment_score(dict_tagged_sentences)
print(score)
