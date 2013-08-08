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

"""A client to create a CLA model for language."""

import csv
import logging

from nupic.frameworks.opf.modelfactory import ModelFactory

import model_params

_LOGGER = logging.getLogger(__name__)

_DATA_PATH = "data/tiny.csv"

_NUM_RECORDS = 100000
_NUM_REPEATS = 1000



def createModel():
  return ModelFactory.create(model_params.MODEL_PARAMS)



def runLanguage():
  model = createModel()
  model.enableInference({'predictedField': 'letter'})
  for r in range(_NUM_REPEATS):
    should_print = r % 5 == 0

    if should_print:
      _LOGGER.info("\n====== Repeat #%d =======\n", r)

    with open (_DATA_PATH) as fin:
      reader = csv.reader(fin)
      headers = reader.next()
      reader.next()
      reader.next()
      for i, record in enumerate(reader, start=1):
        modelInput = dict(zip(headers, record))
        result = model.run(modelInput)
        isLast = i == _NUM_RECORDS
        if should_print:
          prediction = "".join(result.inferences['multiStepBestPredictions'].values())
          _LOGGER.info("Step %i: %s ==> %s", i, modelInput['letter'], prediction)
        if isLast:
          break



if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  runLanguage()
