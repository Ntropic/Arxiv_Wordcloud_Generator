# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 00:52:36 2019

@author: Michael Schilling

Create Wordmaps and wordcounts of n papers in a field of research
"""
search_term="quantum optimal control" #Enter the search term for arxiv
num=50  #Enter the number of papers that are to be downloaded -> A folder for this search term is automatically generated
image_file='..\qoc.png' #A mask image, only the black part of the image will be covered with words
stopwords_input=[] #Words that are not to be included uin the wordmap
max_words=1000 #Maximum words shown in image
                
font = '..\Candal.ttf'
fontcolor='black'
bgcolor = 'white'

import arxiv
import urllib
import urllib2
import requests
import random

from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import sys, getopt

from PIL import Image
from collections import Counter
from PIL import Image
import numpy as np

from nltk.corpus import stopwords 
from wordcloud import WordCloud, STOPWORDS

n=search_term.split()
n="_".join(n)
oldDir=os.path.dirname(os.path.realpath(__file__))
pdfDir = os.path.join(os.path.dirname(os.path.realpath(__file__)),n)
a=arxiv.query(search_query=search_term,max_results=num)

if not os.path.exists(pdfDir):
    os.makedirs(pdfDir)
os.chdir(pdfDir)

def download_file(download_url,path):
    response = urllib2.urlopen(download_url)
    with open(path, 'wb') as file:
        file.write(response.read())
        file.close()
    #print("Completed")
    
def custom_slugify(obj):
    title=obj.title.lower()
    title=title.split()
    title="_".join(title)
    #title.encode('utf8')
    alpha=unicode('abcdefghijklmnopqrstuvwxyz_')
    title=[char for char in title if char in alpha]
    title=''.join(title)
    title=title+'' #add authors in the future?!
    return title

def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    with file(fname, 'rb') as infile:
        for page in PDFPage.get_pages(infile, pagenums):
            interpreter.process_page(page)
        infile.close()
        converter.close()
        text = output.getvalue()
        output.close
    return text 

for i in range(0,len(a)):
    dont=0    
    print(str(i)+'/'+str(len(a)))    
    tit=custom_slugify(a[i])+'.pdf'
    loc=a[i].pdf_url+'.pdf'
    if not os.path.exists(tit):
        print("Downloading... file "+tit)
        try:
            download_file(loc,tit)
        except:
            try:
                print("Downloading... 2nd try for file "+tit)
                if os.path.exists(tit):
                    os.remove(tit)
                download_file(loc,tit)
            except:
                try:
                    if os.path.exists(tit):
                        os.remove(tit)
                    print("Downloading... 3rd try for file "+tit)
                    download_file(loc,tit)
                except:
                    if os.path.exists(tit):
                        os.remove(tit)
                    print('Download of file '+tit+'has failed.')
    
    textFilename = tit
    textFilename = textFilename[0:len(textFilename)-4]+".txt"
    if not os.path.exists(textFilename):
        print("Converting... ")
        try:
            text=convert(tit)
        except:
            try:
                print("Re-Downloading... 2nd try for file "+tit)
                if os.path.exists(tit):
                    os.remove(tit)
                download_file(loc,tit)
                text=convert(tit)
            except:
                if os.path.exists(tit):
                    os.remove(tit)
                print('Re-Download of file '+tit+' has failed.') 
                dont=1
        if dont==0:
            textFile = open(textFilename, "w") #make text file
            textFile.write(text) #write text to text file
            textFile.close()


#converts pdf, returns its text content as a string


def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles

#converts all pdfs in directory pdfDir, saves all resulting txt files to txtdir
def convertMultiple(pdfDir):
    if pdfDir == "": pdfDir = os.getcwd() + "\\" #if no pdfDir passed in 
    for pdf in getListOfFiles(pdfDir): #iterate through pdfs in pdf directory
        fileExtension = pdf.split(".")[-1]
        if fileExtension == "pdf":
            pdfFilename = os.path.join(pdfDir,pdf)
            textFilename = os.path.join(pdfDir,pdf)
            textFilename = textFilename[0:len(textFilename)-4]+".txt"
            if not os.path.exists(textFilename):
                text = convert(pdfFilename) #get string of text content of pdf
                textFile = open(textFilename, "w") #make text file
                textFile.write(text) #write text to text file
            
def concatenateMultiple(pdfDir, txtDir2):
    if pdfDir == "": pdfDir = os.getcwd() + "\\" #if no pdfDir passed in 
    text=''
    for txt in getListOfFiles(pdfDir): #iterate through pdfs in pdf directory
        fileExtension = txt.split(".")[-1]
        if fileExtension == "txt":
            txtFilename = os.path.join(pdfDir,txt)
            filena=open(txtFilename,'r')
            text =text+' '+filena.read() #get string of text content of pdf

    textFile = open(txtDir2, "w+") #make text file
    textFile.write(text) #write text to text file
    
def grey_color(word, font_size, position, orientation, random_state=None, **kwargs):
    return 'hsl(0, 0%%, %d%%)' % random.randint(0, 20)
    


pdfDir=pdfDir+'\\'                  
convertMultiple(pdfDir)
txtDir2 = pdfDir+'conc_txt.txt'
concatenateMultiple(pdfDir, txtDir2)

#Create Wordmap with all words
#open and concatenate all textfiles
text=open(txtDir2,'r')
data=text.read().lower()

lister=['arxivhep-th','fig','nucl','eld','hep-th','hep','th','arxivhep','arxiv','um','et','al','rev','lett','phys','rev','et al','rev lett','phys rev','=','-','cid','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','.',',',';',':','+','*']
lister.extend(stopwords_input)
stop_words=stopwords.words('english')
stop_words=[x.encode('UTF8') for x in stop_words]
stop_words.extend(lister)

data = [char for char in data if char in 'abcdefghijklmnopqrstuvwxyz -']
data=''.join(data)
data=data.replace("cid", " ") 
b=data.split()
words=[w for w in b if not w in stop_words]

#words = data.split(" ")
num_words = len(words)
print("The number of words is ", num_words)

c=Counter(words)
d=c.most_common(100)
print(d)
    
all_text=" ".join(words)

if len(image_file)>0:
    ns_mask=np.array(Image.open(image_file))
    wc = WordCloud(background_color=bgcolor, max_words=max_words,max_font_size=150,stopwords=stop_words,width=ns_mask.shape[1], height=ns_mask.shape[0],mask=ns_mask, contour_width=1,font_path=font)    
else:
    wc = WordCloud(background_color=bgcolor, max_words=max_words,max_font_size=150,stopwords=stop_words,width=2000, height=1100, contour_width=1,font_path=font)    

wc.generate(all_text)
wc.recolor(color_func=grey_color, random_state=3)
wc.to_file(os.path.join(pdfDir,n+'_word_cloud.png'))
  
os.chdir(oldDir)