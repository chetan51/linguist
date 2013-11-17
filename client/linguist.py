#!/usr/bin/env python
# ----------------------------------------------------------------------
# Chetan Surpur
# Copyright (C) 2013
#
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have purchased from
# Numenta, Inc. a separate commercial license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

"""A client to create a CLA model for Linguist."""

import sys
from nupic.frameworks.opf.modelfactory import ModelFactory
import model_params
import re

NUM_REPEATS = 5
PRINT_EVERY_REPEAT_N = 1

TERMINATORS = ['.','!','?','|','\n']
NUM_SENTENCES = 5 # number for story sentences generated
STORY_START = "The dog" 
_QUIT = "QUIT"

def clean(s):
  return re.sub('\n', '|', s)

def prediction(inferences):
  return clean("".join(inferences['multiStepBestPredictions'].values()))

def confidences(inferences):
  c = ""
  predictions = inferences['multiStepPredictions']
  bestPredictions = inferences['multiStepBestPredictions']

  for i in bestPredictions:
    v = bestPredictions[i]
    prediction = predictions[i]

    if v in prediction:
      probability = prediction[v]
    else:
      probability = 0

    c += format(probability, ".2f")

    if i < len(bestPredictions):
      c += " | "

  return c

def createModel():
  return ModelFactory.create(model_params.MODEL_PARAMS)

def runLinguist(datapath):
  model = createModel()
  model.enableInference({'predictedField': 'letter'})

  i = 1
  for r in range(NUM_REPEATS):
    should_print = r % PRINT_EVERY_REPEAT_N == 0

    if should_print:
      print "\n====== Repeat #%d =======\n" % (r + 1)

    with open(datapath) as f:
      while True:
        c = f.read(1)
        if not c: break

        if not ( (ord(c) >= 31 and ord(c) <= 127) or c == '\n'): continue

        modelInput = {'letter': c}
        result = model.run(modelInput)
        if should_print:
          print "[%i]\t %s ==> %s\t(%s)" % (i, clean(modelInput['letter']), prediction(result.inferences), confidences(result.inferences))
        if c in TERMINATORS:
          model.resetSequenceStates()
          print "reset"

        i += 1

  return model

def tellStory(model, startSent, lenght):
  """feed startSent sequence and then continue to generate the story by the CLA. 
    param model: the trained CLA model
    param startSent: starting sequence as a string, eg \"And so he raised the gun\" 
    param lenght: #sequences to generate. """

  model.disableLearning()
  for s in startSent:
    print(s),
    modelInput = {'letter': s}
    result = model.run(modelInput)

  numSent = 0
  c = s
  sentence_len = 0
  while numSent <= lenght:
    print(c),
    modelInput = {'letter': c}
    result = model.run(modelInput)
    c=result.inferences['prediction'][0]
    
    sentence_len += 1
    if(sentence_len > 30): #limit, sometimes there's no sentence terminator generated and we'd run forever
      numSent += 1
      sentence_len = 0

    if c in TERMINATORS:
      numSent += 1
      sentence_len = 0
      print(' \n')


if __name__ == "__main__":
  if len(sys.argv) > 1:
    datapath = sys.argv[1]
    if len(sys.argv) > 2:
      NUM_REPEATS = int(sys.argv[2])
      if len(sys.argv) > 3:
        NUM_SENTENCES = int(sys.argv[3])

    model = runLinguist(datapath)
    print('==========================================')
    print('Welcome young adventurer, let me tell you a story! ')
    while True: 
      STORY_START = raw_input('Enter story start (QUIT to go to work): ')
      if(STORY_START == "QUIT"): 
        break
      tellStory(model, STORY_START, NUM_SENTENCES)

    print('Farewell')
  else:
    print "Usage: python linguist.py path/to/data.txt [num_repeats [num_sentences]]"
