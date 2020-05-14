from logging import getLogger
from queue import Queue
from typing import Callable


def processor(source: Queue, process: Callable, destination: Queue=None):
  """Calls `process` on the `source` queue items.
  Results are put in `destination,` if specified
  """
  logger = getLogger()

  while True:
    item = source.get()
    try:
      processed_item = process(item)
    except:
      logger.error(f'Exception caught processing {item}.', exc_info=True)

    if destination is not None:
      destination.put(processed_item)

    source.task_done()


def fork_processor(source: Queue, process: Callable, predicate: Callable, left_destination: Queue, right_destination: Queue):
  """Calls `process` on the `source` queue items.
  `predicate` is called on each result; `True` results are put in the
  `left_destination` queue, `False` are put in the `right_destination` queue.
  """
  logger = getLogger()

  while True:
    item = source.get()
    try:
      processed_item = process(item)
    except:
      logger.error(f'Exception caught processing {item}.', exc_info=True)

    if type(processed_item) is list:
      for processed in processed_item:
        if predicate(processed):
          left_destination.put(processed)
        else:
          right_destination.put(processed)
    else:
      if predicate(processed_item):
        left_destination.put(processed_item)
      else:
        right_destination.put(processed_item)

    source.task_done()
