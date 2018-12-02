import argparse

def get_args():
    parser = argparse.ArgumentParser(
        description="Run a solution by specifying a day and a star."
    )
    parser.add_argument(
        'day',
        type=int,
        help="The day to run the solution(s) of."
    )
    parser.add_argument(
        'star',
        nargs='?',
        default=None,
        type=int,
        choices=(1,2),
        help="The star of the solution to run. Omit to run all stars."
    )
    args = parser.parse_args()
    return args.day, args.star

def main():
    day,star = get_args()

    try:
        module = __import__('day' + str(day))
    except ModuleNotFoundError:
        print("Day hasn't been solved yet.")
        return

    if star is None or star == 1:
        try:
            f = module.star1
        except AttributeError:
            print("First star hasn't been solved yet.")
        else:
            print("Star 1:")
            f()

    if star is None or star == 2:
        try:
            f = module.star2
        except AttributeError:
            print("Second star hasn't been solved yet.")
        else:
            if star is None:
                print()
            print("Star 2:")
            f()

if __name__ == '__main__':
    main()
