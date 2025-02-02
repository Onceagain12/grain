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

"""TensorFlow ops for interacting with ArrayRecord files."""
import hashlib
import os
import pathlib
from typing import Any, Callable, Mapping, Optional, Sequence, Union

from etils import epath
from grain._src.core import usage_logging
from grain._src.tensorflow.ops import gen_array_record_ops
import tensorflow as tf


TfParseFn = Callable[[tf.Tensor], Mapping[str, Any]]


class TfArrayRecordDataSource:
  """A random access data source for reading from ArrayRecord files.

  Example usage:
    ar = gtf.ArrayRecord("/tmp/foo@*")
    # Create dataset with keys. Keys must be in [0, len(ar) - 1].
    keys_dataset = tf.data.Dataset.range(len(ar))
    # Batch lookup for better performance.
    dataset = keys_dataset.batch(128).map(lambda i: ar[i]).unbatch()
  """

  def __init__(
      self,
      paths: Union[epath.PathLike, Sequence[epath.PathLike]],
      parse_fn: Optional[TfParseFn] = None,
      cache: bool = False,
      shared_name: Optional[str] = None,
  ):
    """Creates a new TfArrayRecordDataSource object.

    Args:
      paths: This can be a single path or list of paths. A path can be a single
        filename, a sharded pattern, sharded spec or a read instruction string.
        A read instruction string is of the form 'filename[start:end]' where
        only records within the range [start, end) should be read. When you want
        to read subsets or have a large number of files prefer to path read
        instructions. This makes the initialization faster.
      parse_fn: Optional function to parse records.
      cache: Whether to cache values in memory. This will cache uncompressed
        (but still serialized) values after they are read the first time. This
        can use a lot of memory but can improve performance when iterating over
        the data source many time.
      shared_name: Name for the resource. If a resource with the name already
        exists it will be reused. If not set will use a hash of the paths. This
        should the resource if you create multiple ArrayRecord objects for the
        same set of paths.
    """
    if isinstance(paths, (str, pathlib.Path)):
      paths = [paths]
    # Convert Path objects to strings.
    paths = [os.fspath(p) for p in paths]
    if shared_name is None:
      h = hashlib.sha1()
      h.update(str(paths).encode())
      shared_name = h.hexdigest()
    self._paths = paths
    self._parse_fn = parse_fn
    self._shared_name = shared_name
    self._handle = gen_array_record_ops.array_record_resource_handle(
        paths=self._paths, cache=cache, shared_name=self._shared_name
    )
    usage_logging.log_event(
        "TfArrayRecordDataSource", tag_2="ARRAY_RECORD", tag_3="TfGrain"
    )

  def __len__(self) -> int:
    t = gen_array_record_ops.array_record_num_records(self._handle)
    return t.numpy().item()

  def __getitem__(self, record_keys: tf.Tensor) -> tf.Tensor:
    return gen_array_record_ops.array_record_lookup(self._handle, record_keys)

  # For easy integration with Grain. Subclasses should override this.
  def get_parse_fn(self) -> Optional[TfParseFn]:
    return self._parse_fn

  def __repr__(self) -> str:
    h = hashlib.sha1()
    for p in self._paths:
      h.update(p.encode())
    return f"TfArrayRecordDataSource(hash_of_paths={h.hexdigest()})"
