import json
from queue import Queue
from threading import Event

result_queue = Queue()


def Error_checker():
    try:
      with open("counters/error.json", 'r') as json_file:
          error = json.load(json_file)
      if error == 1:
        result_queue.put(True)
      else:
        result_queue.put(False)
    except Exception as e:
      result_queue.put(True)

if __name__ == "__main__":
    Error_checker()

def Error_checker_result():
    return result_queue.get()
correction  = Error_checker()