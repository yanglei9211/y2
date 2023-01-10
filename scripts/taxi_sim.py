import collections
import queue
import random

DEFAULT_NUMBER_OF_TAIXS = 3
DEFAUAL_END_TIME = 160
SEARCH_DURATION = 5
TRIP_DURATION = 20
DEPARTURE_INTERVAL = 5

Event = collections.namedtuple('Event', 'time proc action')


def taxi_process(ident, trips, start_time=0):
    time = yield Event(start_time, ident, 'leave garage')
    for i in range(trips):
        time = yield Event(time, ident, 'pick up')
        time = yield Event(time, ident, 'drop off')
    yield Event(time, ident, 'going home')

def compute_duration(previous_action):
    if previous_action in ['leave garage', 'drop off']:
        interval = SEARCH_DURATION
    elif previous_action == 'pick up':
        interval = TRIP_DURATION
    elif previous_action == 'going home':
        interval = 1
    else:
        raise ValueError('unknown action: {}'.format(previous_action))
    return int(random.expovariate(1.0/interval))+1


class Simulator:
    def __init__(self, procs_map):
        self.events = queue.PriorityQueue()
        self.procs = dict(procs_map)

    def run(self, end_time):
        for _, proc in sorted(self.procs.items()):
            f_event = next(proc)
            self.events.put(f_event)

        sim_time = 0
        while sim_time < end_time:
            if self.events.empty():
                print("*** end of events ***")
                break
            current_event = self.events.get()
            sim_time, proc_id, previous_action = current_event
            print("taxi: ", proc_id, proc_id * '  ', current_event)
            active_proc = self.procs[proc_id]
            next_time = sim_time + compute_duration(previous_action)
            try:
                next_event = active_proc.send(next_time)
            except StopIteration:
                del self.procs[proc_id]
            else:
                self.events.put(next_event)
        else:
            msg = '*** end of simulation time: {} events pending ***'
            print(msg.format(self.events.qsize()))


def main(end_time=DEFAUAL_END_TIME, num_taxis=DEFAULT_NUMBER_OF_TAIXS,
         seed=None):
    if seed is not None:
        random.seed(seed)
    taxis = {i: taxi_process(i, (i+1)*2, i*DEPARTURE_INTERVAL)
             for i in range(num_taxis)}
    sim = Simulator(taxis)
    sim.run(end_time)

if __name__ == '__main__':
    main(DEFAUAL_END_TIME, 2, 10)