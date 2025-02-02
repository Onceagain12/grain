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
"""APIs for using Grain on top of tf.data."""

# pylint: disable=g-multiple-import
# pylint: disable=unused-import
# pylint: disable=wildcard-import

from . import tensorflow_experimental as experimental

from ._src.tensorflow.batching import (
    TfBatch,
    TfBatchAndPack,
    TfBatchFn,
    TfBatchNone,
    TfBatchWithPadElements,
)
from ._src.tensorflow.checkpoint_handlers import OrbaxCheckpointHandler
from ._src.tensorflow.data_iterators import (
    ArraySpec,
    IteratorOptions,
    DatasetIterator,
    TfGrainDatasetIterator,
)
from ._src.tensorflow.data_loaders import (
    load_from_tfds,
    TfDataLoader,
    TfMixtureDataLoader,
)
from ._src.tensorflow.data_sources import (
    TfArrayRecordDataSource,
    TfDataSource,
    TfdsDataSource,
    TfInMemoryDataSource,
    TfParseFn,
)
from ._src.tensorflow.index_dataset import (
    Index,
    FirstIndex,
    NextIndex,
    TfIndexSampler,
    TfDefaultIndexSampler,
    TfMixtureIndexSampler,
)
from ._src.tensorflow.transforms import (
    CacheTransform,
    IgnoreErrorsTransform,
    FilterTransform,
    MapTransform,
    RandomMapTransform,
    Transformation,
    Transformations,
    UnsafeTfDataTransform,
)

from .core import *
