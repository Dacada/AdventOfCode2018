import util
from datetime import datetime

DAY = 4

def parse_entry(entry):
    date = datetime.strptime(entry[entry.index('[')+1:entry.index(']')], '%Y-%m-%d %H:%M')
    if '#' in entry:
        event = int(entry[entry.index('#')+1:entry.index(' ',entry.index('#'))])
    elif 'falls' in entry:
        event = 'begin'
    elif 'wakes' in entry:
        event = 'end'
    else:
        raise Exception("Unknown event for entry: " + entry)
    return (date,event)

def parse_input(input):
    minutes = {}
    current_guard = None
    start_asleep_datetime = None
    
    for entry in sorted((parse_entry(e) for e in input), key=lambda e: e[0]):
        date,event = entry
        if type(event) is int:
            current_guard = event
            if current_guard not in minutes:
                minutes[current_guard] = [0]*60
        elif event == 'begin':
            start_asleep_datetime = date
            if current_guard is None:
                raise Exception("Unexpected fall asleep event, guard didn't start yet.")
        elif event == 'end':
            if current_guard is None:
                raise Exception("Unexpected wake up event, guard didn't start yet.")
            l = minutes[current_guard]
            for i in range(start_asleep_datetime.minute, date.minute):
                l[i] += 1

    return minutes

@util.timing_wrapper
def star1():
    minutes = parse_input(util.get_input_lines(DAY))
    chosen_guard = max(minutes.items(), key=lambda x: sum(x[1]))[0]
    chosen_minute = max(range(60), key=lambda x: minutes[chosen_guard][x])
    return chosen_guard*chosen_minute

@util.timing_wrapper
def star2():
    minutes = parse_input(util.get_input_lines(DAY))
    
    best_frequency = 0
    for guard in minutes:
        best_guard_minute = max(range(60), key=lambda x: minutes[guard][x])
        frequency = minutes[guard][best_guard_minute]
        if frequency > best_frequency:
            best_frequency = frequency
            best_minute_overall = best_guard_minute
            best_guard = guard

    return best_guard*best_minute_overall

if __name__ == '__main__':
    util.pretty_print(star1, star2)
