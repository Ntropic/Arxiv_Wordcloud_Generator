# Arxiv_Wordcloud_Generator
## This Python 2.7 Script creates wordmaps from the first *n* papers of an *arxiv* search.

### Explanation:
In the beginning of *filegrabber.py*, a number of parameters can be defined, most notably:
* *search_term* for initiating the search in arxiv
* *num* the number of papers, that are to be downloaded
* *image_file* defines an image, so that only the black parts are covered by the wordcloud (can be an empty string if not desired)
* *stopwords_input* Define words, that are not taken into account in the wordcloud, these get added to a preexisting list of such words. The conversion of a *pdf* into a text file can lead to the emergence of unwanted symbols from formulas, graphics or journal names. 
* *max_words* defines the number of words that are shown in the wordcloud

### Example:
For the search term **Quantum Optimal Control**, the first *50* arxiv papers and an example background image, lead to the following output:
<p align="center">
<img src="https://github.com/Ntropic/Arxiv_Wordcloud_Generator/blob/master/quantum_optimal_control/quantum_optimal_control_word_cloud.png?raw=true" width="700" height="330" />
</p>
<p align="center"> 
QOC - Quantum Optimal Control with 1000 words.
</p>

### Installation:
The script *filegrabber.py* requires Python 2.7 with the following packages, that can be installed using *pip -install*:
* *arxiv* An arxiv API
* *urllib* & *urllib2*
* *requests*
* *cStringIO*
* *pdfminer*
* *PIL*
* *numpy*
* *nltk*
* *wordcloud*
