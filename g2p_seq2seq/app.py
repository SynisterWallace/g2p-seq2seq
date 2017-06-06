# Copyright 2016 AC Technologies LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Binary for training translation models and decoding from them.

See the following papers for more information on neural translation models.
 * http://arxiv.org/abs/1409.3215
 * http://arxiv.org/abs/1409.0473
 * http://arxiv.org/abs/1412.2007
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import codecs
import tensorflow as tf

from g2p_seq2seq.g2p import G2PModel
from g2p_seq2seq.params import Params

import yaml
from six import string_types

#from seq2seq import tasks, models
#from seq2seq.configurable import _maybe_load_yaml, _deep_merge_dict
#from seq2seq.data import input_pipeline
#from seq2seq.inference import create_inference_graph
#from seq2seq.training import utils as training_utils

#from IPython.core.debugger import Tracer

tf.flags.DEFINE_string("model", None, "Training directory.")
tf.flags.DEFINE_boolean("interactive", False,
                        "Set to True for interactive decoding.")
tf.flags.DEFINE_string("evaluate", "", "Count word error rate for file.")
tf.flags.DEFINE_string("decode", "", "Decode file.")
tf.flags.DEFINE_string("output", "", "Decoding result file.")
tf.flags.DEFINE_string("train", "", "Train dictionary.")
tf.flags.DEFINE_string("valid", "", "Development dictionary.")
tf.flags.DEFINE_string("test", "", "Test dictionary.")
tf.flags.DEFINE_boolean("reinit", False,
                            "Set to True for training from scratch.")
# Training parameters
tf.flags.DEFINE_integer("batch_size", 64,
                        "Batch size to use during training.")
tf.flags.DEFINE_integer("max_steps", 500,
                        "How many training steps to do until stop training"
                        " (0: no limit).")
tf.flags.DEFINE_integer("eval_every_n_steps", 200,
                        "Run evaluation on validation data every N steps.")
tf.flags.DEFINE_string("hooks", "",
                       """YAML configuration string for the
                       training hooks to use.""")
tf.flags.DEFINE_string("model_params", "",
                       """YAML configuration string for the model
                       parameters.""")
tf.flags.DEFINE_string("metrics", "",
                       """YAML configuration string for the
                       training metrics to use.""")
tf.flags.DEFINE_string("input_pipeline", None,
                       """Defines how input data should be loaded.
                       A YAML string.""")
# RunConfig Flags
tf.flags.DEFINE_integer("save_checkpoints_secs", None,
                        """Save checkpoints every this many seconds.
                        Can not be specified with save_checkpoints_steps.""")
tf.flags.DEFINE_integer("save_checkpoints_steps", None,
                        """Save checkpoints every this many steps.
                        Can not be specified with save_checkpoints_secs.""")

FLAGS = tf.app.flags.FLAGS

def main(_=[]):
  """Main function.
  """

  if FLAGS.save_checkpoints_secs is None \
    and FLAGS.save_checkpoints_steps is None:
    FLAGS.save_checkpoints_secs = 600
    tf.logging.info("Setting save_checkpoints_secs to %d",
                    FLAGS.save_checkpoints_secs)

  with tf.Graph().as_default():
    if not FLAGS.model:
      raise RuntimeError("Model directory not specified.")
    g2p_model = G2PModel(FLAGS.model)
    if FLAGS.train:
      g2p_params = Params(decode_flag=False, flags=FLAGS)
      g2p_model.load_train_model(g2p_params)
      #if (not os.path.exists(os.path.join(FLAGS.model,
      #                                    "model.data-00000-of-00001"))
      #    or FLAGS.reinit):
      #  g2p_model.create_train_model(g2p_params)
      #else:
      #  g2p_model.load_train_model(g2p_params)
      g2p_model.train()
    else:
      g2p_params = Params(decode_flag=True, flags=FLAGS)
      g2p_model.load_decode_model(g2p_params)
      #if FLAGS.decode:
        #Tracer()()
      #  g2p_model.decode()
        #decode_lines = codecs.open(FLAGS.decode, "r", "utf-8").readlines()
        #output_file = None
      #  if FLAGS.output:
      #    output_file = codecs.open(FLAGS.output, "w", "utf-8")
        #g2p_model.decode(decode_lines, output_file)
      #elif FLAGS.interactive:
      #  g2p_model.interactive()
      #elif FLAGS.evaluate:
      #  test_lines = codecs.open(FLAGS.evaluate, "r", "utf-8").readlines()
      #  g2p_model.evaluate(test_lines)

if __name__ == "__main__":
  tf.logging.set_verbosity(tf.logging.INFO)
  tf.app.run()
