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

NUM_REPEATS = 1000
PRINT_EVERY_REPEAT_N = 1

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

    last_c = ''

    with open(datapath) as f:
      while True:
        c = f.read(1)
        if not c: break

        if ord(c) <= 31 and ord(c) >= 127: continue
        if last_c == ' ' and c == last_c: continue

        last_c = c

        modelInput = {'letter': c}
        result = model.run(modelInput)

        if should_print:
          prediction = "".join(result.inferences['multiStepBestPredictions'].values())
          print "[%i]\t %s ==> %s" % (i, modelInput['letter'], prediction)

        i += 1


if __name__ == "__main__":
  if len(sys.argv) > 1:
    datapath = sys.argv[1]
    runLinguist(datapath)
  else:
    print "Usage: python linguist.py [path/to/data.txt]"
