'''
This program is a shell which opens CSV files, reads the column and writes a new file containing a sentiment score
'''

import sentlex
import sentlex.sentanalysis
import csv

#in the format of r'C:\Python27\refugee_scrape\refugee_scrape\spiders\sentimentfile.csv'
fieldnames=['dateCreated', 'time', 'message', 'userLocation','voteRating','voteCount','assetHeadline','assetUrl']
f=open(r'C:\Python27\refugee_scrape\refugee_scrape\spiders\sentimentfile.csv','a+')
newf=open(r'C:\Python27\refugee_scrape\refugee_scrape\spiders\sentimentfile_scored.csv','a+')
data_array=csv.DictReader(f,fieldnames=fieldnames,delimiter=',') #returns an iterable of dictionaries with the fieldnames attached
#print data_array
for row in data_array:
    input_text=row['message']
    SWN=sentlex.SWN3Lexicon()
    classifier = sentlex.sentanalysis.BasicDocSentiScore()
    #may want these arguements passed into the function
    classifier.classify_document(input_text,tagged=False,L=SWN,a=True, v=True, n=False, r=False, negation=True, verbose=False)
    #print classifier.resultdata for positive and negative score
    #append dictionary with appropriate tags
    positive=classifier.resultdata['resultpos']
    negative=classifier.resultdata['resultneg']
    total=positive-negative
    #maybe we want to pickle this?
    row['positiveScore']=str(positive)
    row['negativeScore']=str(negative)
    row['totalScore']=str(total)
    
    #print row.values()

    #There is a better method for this using row.values() or creating a list of keys

    newrow=row['dateCreated'] + "," + row['time'] + "," + row['message'] + "," + row['userLocation'] + "," + row['voteRating'] + "," + row['voteCount'] + "," + row['assetHeadline'] + "," + row['assetUrl'] + "," + row['positiveScore'] + "," + row['negativeScore'] + "," + row['totalScore']
    newf.write(str(newrow)+'\n')

##    newfieldnames=['dateCreated', 'time', 'message', 'userLocation','voteRating','voteCount','assetHeadline','positiveScore','negativeScore','totalScore']
##    writer=csv.DictWriter(newf,fieldnames=newfieldnames, delimiter=',')
##    writer.writerow(row['dateCreated', 'time', 'message', 'userLocation','voteRating','voteCount','assetHeadline','positiveScore','negativeScore','totalScore'])

f.close()
newf.close()


##def sentiment_append(csv_pointer):
##    #in the format of r'C:\Python27\refugee_scrape\refugee_scrape\spiders\sentimentfile.csv'
##    fieldnames=['dateCreated', 'time', 'message', 'userLocation','voteRating','voteCount','assetHeadline']
##    f=open(csv_pointer,'a+')
##    #newf=open(r'C:\Python27\refugee_scrape\refugee_scrape\spiders\sentimentfile_scored.csv','a+')
##    data_array=csv.DictReader(f,fieldnames=fieldnames,delimiter=',') #returns an iterable of dictionaries with the fieldnames attached
##    #print data_array
##    for row in data_array:
##        input_text=row.data_array['message']
##        print input_text
##        #possible append this to add triple '''
##        SWN=sentlex.SWN3Lexicon()
##        classifier = sentlex.sentanalysis.BasicDocSentiScore()
##        #may want these arguements passed into the function
##        classifier.classify_document(input_text,tagged=False,L=SWN,a=True, v=True, n=False, r=False, negation=True, verbose=False)
##        #print classifier.resultdata for positive and negative score
##        #append dictionary with appropriate tags
##        positive=classifier.resultdata['resultpos']
##        negative=classifier.resultdata['negative']
##        total=positive-negative
##        data_array['positiveScore']=positive
##        data_array['negativeScore']=negative
##        data_array['totalScore']=total
##
##        newfieldnames=['dateCreated', 'time', 'message', 'userLocation','voteRating','voteCount','assetHeadline','positiveScore','negativeScore','totalScore']
##        
##
##        #write new column for positive, new column for negative
##        #return
##    f.close()
##    #newf.close()
##    return
##
##        
##    
##sentiment_append(r'C:\Python27\refugee_scrape\refugee_scrape\spiders\sentimentfile.csv')


##input_text='''we had a great time at the tirreno hotel, very friendly and helpful, nothing was ever too much trouble. 
##the rooms were in excellent condition, very clean and comfortable.'''
##SWN=sentlex.SWN3Lexicon()
##
##classifier = sentlex.sentanalysis.BasicDocSentiScore()
##
##classifier.classify_document(input_text,tagged=False,L=SWN,a=True, v=True, n=False, r=False, negation=True, verbose=False)
##'''
## Classify an input document with classifier parameters per kwargs.
##   Doc - string, inoput document.
##   tagged - indicate wheter document is POS-tagged (False will call NLTK's default tagger)
##   verbose - debug messages printed.
##   **kwargs - classifier-specific parameters (optional). 
##
## When subclassing the default classifier, classify_doc (the algorithm)
## and set_parameters (parse algo parameters) need to be implemented.
##
## The following are mandatory parameters for every classifier algorithm:
##   L - a sentiment lexicon (sentlex.Lexicon object);
##   a,v,r,n - POS tags to scan (booleans);
##   negation - boolean
##   negation_window - integer
##'''
##print classifier.resultdata
