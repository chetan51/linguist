Linguist
========

An AI running on [NuPIC](https://github.com/numenta/nupic) using the CLA to build a model of language, and predict the rest of a user's word, phrase, sentence.

The current application works as a "story teller", it'll train on a dataset you give it and then produce a story for you. You can specify number of sentences the story 
should have and the beginig words to kick off "There were two brothers ". 

Research: 

The CLA learns sentences letter-by-letter, we'd like to observe if grammatical features can emerge. See [Jeff Hinton's text-generation deep NNs](https://class.coursera.org/neuralnets-2012-001/lecture/91) for reference. 

Usage
========

First, install [NuPIC](https://github.com/numenta/nupic).

Then, run:

    python client/linguist.py data/tiny.txt

It'll run on the tiny.txt dataset, feeding it the sentence over and over again, printing out Linguist's next 10 timestep predictions at each step.
