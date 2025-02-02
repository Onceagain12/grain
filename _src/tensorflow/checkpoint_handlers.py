# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This module provides a CheckpointHandler for integration with Orbax."""
from typing import Any

from etils import epath
from grain._src.tensorflow import data_iterators
import jax

TfGrainDatasetIterator = data_iterators.TfGrainDatasetIterator


# Implements orbax.checkpoint.CheckpointHandler
class OrbaxCheckpointHandler:
  """Orbax CheckpointHandler for DataIterator."""

  def save(self, directory: epath.Path, item: TfGrainDatasetIterator):
    filename = (
        directory
        / f"process_{jax.process_index()}-of-{jax.process_count()}.json"
    )
    item.save(filename)

  def restore(
      self, directory: epath.Path, item: TfGrainDatasetIterator
  ) -> TfGrainDatasetIterator:
    """Restores the given iterator from the checkpoint in `directory`."""
    if item is None:
      raise ValueError("OrbaxCheckpointHandler requires `item`.")
    filename = (
        directory
        / f"process_{jax.process_index()}-of-{jax.process_count()}.json"
    )
    if not filename.exists():
      raise ValueError(f"File {filename} does not exist.")
    item.restore(filename)
    return item

  # Required by interface but not supported by Grain checkpoints.
  def structure(self, directory: epath.Path) -> Any:
    del directory
    return None
