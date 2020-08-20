import docx2txt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from collections import Counter
import io
import os
import re
import nltk
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import spacy
from spacy.matcher import Matcher

def process(file):
    stat = dict()
    for filename in os.listdir("./test_job"):
        # Store the job description into a variable
        job_description = docx2txt.process("./test_job/"+filename)

        # Print the job description
        # print(job_description)

        # A list of text
        text = [resume, job_description]

        cv = CountVectorizer()
        count_matrix = cv.fit_transform(text)
        #get the match percentage
        matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
        matchPercentage = round(matchPercentage, 2) # round to two decimal
        stat[(resume,filename)] = matchPercentage
        print("Your resume matches about "+ str(matchPercentage)+ "% of the job description:"+ filename)

    match = Counter(stat)
    top5 = match.most_common(5)
    output = 'Your top job recommendations are:'
    for (temp_resume,temp_match) in top5:
        print(temp_resume[1],temp_match,"% matching")
        output += "\n"+str(temp_resume[1][:-5])+" "+str(temp_match)+" % macthing"+"|"
    print(output)
    return output

