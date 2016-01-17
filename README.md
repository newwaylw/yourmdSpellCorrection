# Your.md spell correction service

## Software requirements
You will need to have the following softwares installed to run this program.
* [Python3](https://www.python.org/download/releases/3.0/)
* [Python Flask](http://flask.pocoo.org/)
* Python numpy, scipy, pandas. you make want to install packages such as [Anaconda](https://www.continuum.io/downloads)

## Usage
Make sure you plaform satisfies the above mentioned requirements. then execute within the script folder:

    python3 spell_service.py

A local web server should be running at 
http://localhost:5000

make your requests to http://localhost:5000/<word>, e.g. http://localhost:5000/thoat

It will return a list (default 3) of suggested candidates in descending score order.

# Method

The spell correction is based on edit distance and (cosine) distance between two word vectors. The scoring function is:
    
    score(w1,w2) = p(w2) / (exp(ed(w1,w2)+d(w1,w2)))  
where:
* *w1* denotes the target (input) word, while *w2* is a candiate word.
* *p(w)* denotes the unigram probability of word *w*
* *ed(w1,w2)* denotes the edit distance between *w1* and *w2*
* *d(w1,w2)* denotes the cosine distance between *w1* and *w2*

To calculate cosine distance, I used [word2vec](https://code.google.com/p/word2vec/) utility on the query data to produce word vectors for each word. this is stored as symptom.vec

The idea is that I hope to capture the similarity between words, so that correctly spelled words and various mis-spelled versions will stay 'close', because they are used in a similar context (e.g. to describe similar symptons). I've also produced a t-sne manifold file (symptom.tsne) on the word vectors for visualization.

Also the edit distance is slightly modified so that a penalty is applied if the first letter is different (e.g. users are very unlikely to mistype the first letter)

# Other ideas worth trying (but haven't)
We can include the key distributions in a keyboard to improve the edit distance. For example keys that are close together will have a higher probability of mistakes than farther keys. Like this person have done: https://github.com/ekta1007/Custom-Distance-function-for-typos-in-hand-generated-datasets-with-QWERY-Keyboard/blob/master/QWERT_ver2.py

