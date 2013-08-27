Linguist
========

An AI running on NuPIC using the CLA to build a model of language, and predict the rest of a user's word, phrase, sentence.

Usage
========

First, install [NuPIC](https://github.com/numenta/nupic).

Then, run:

    python client/linguist.py data/tiny.txt

It'll run on the tiny.txt dataset, feeding it the sentence over and over again, printing out Linguist's next 10 timestep predictions at each step.