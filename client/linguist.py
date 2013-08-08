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

import logging
from nupic.frameworks.opf.modelfactory import ModelFactory
import model_params

LOG = logging.getLogger(__name__)
DATA_PATH = "data/tiny.txt"
NUM_REPEATS = 1000

def createModel():
  return ModelFactory.create(model_params.MODEL_PARAMS)

def runLanguage():
  model = createModel()
  model.enableInference({'predictedField': 'letter'})

  for r in range(NUM_REPEATS):
    should_print = r % 5 == 0

    if should_print:
      LOG.info("\n====== Repeat #%d =======\n", r)

    i = 1
    
    with open(DATA_PATH) as f:
      while True:
        c = f.read(1)
        if not c: break

        modelInput = {'letter': c}
        result = model.run(modelInput)

        if should_print:
          prediction = "".join(result.inferences['multiStepBestPredictions'].values())
          LOG.info("Step %i:\t %s ==> %s", i, modelInput['letter'], prediction)

        i += 1


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  runLanguage()
