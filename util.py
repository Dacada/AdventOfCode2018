import os
import time
import traceback

def _get_filename(day):
    return 'input' + str(day) + '.txt'

def get_input_lines(day):
    """Read the day's input file and yield each line, without the newline
    character.

    """
    filename = _get_filename(day);
    with open(filename) as f:
        for line in f:
            yield line.strip()

def get_input_text(day):
    """Get whole text of the input file"""
    filename = _get_filename(day)
    with open(filename) as f:
        text = f.read()
    return text.strip()

def timing_wrapper(fun):
    """Decorator. Call fun with no arguments, timing it and nicely
    printing its return value and taken time

    """
    def f():
        start = time.perf_counter() #python3.3
        try:
            result = fun()
        except BaseException as e:
            error = e
            tb = traceback.format_exc()
        else:
            error = None
        finally:
            end = time.perf_counter()

        print("Time taken: {:.5f} seconds".format(end - start))
        if error is None:
            print("Result:", result)
        else:
            print("Exception raised. Traceback follows.")
            print(tb)
    return f

def pretty_print(star1, star2):
    print("Star 1:")
    star1()
    print()
    print("Star 2:")
    star2()
