import random

def work(func):
    def helper(*args, **kwargs):
        variable = func(*args, **kwargs)
        variable.send(None)
        return variable
    return helper

class State:
    def __init__(self, name, possible_to_go):
        self.name = name
        self.possible_to_go = possible_to_go

    def __str__(self):
        return self.name
        # result = ""
        # for state in self.states:
        #     result += state
        # return result


class Day:
    def __init__(self, characteristics=None):
        self.study = State('study', ["walk", "eat", 'sleep', 'volunteer', 'relax'])
        self.walk = State("walk", ["relax", "study", "volunteer"])
        self.eat = State("eat", ["relax", "walk"])
        self.volunteer = State("volunteer", ["walk", "study"])
        self.wash = State("wash", ["study", "eat", "sleep"])
        self.relax = State("relax", ["study", "volunteer", "eat"])
        self.sleep = State("sleep", ["eat", "wash", "study"])

        if not characteristics:
            self.characteristics = []
        else:
            self.characteristics = characteristics
        self.current_state = self.sleep
        self.stopped = False

    def add_state(self, state):
        self.characteristics.append(state)

    def delete_state(self, state):
        self.characteristics.remove(state)

    def send(self, action):
        try:
            self.change().send(action)
        except StopIteration:
            self.stopped = True

    def finite(self):
        result = 'To sum up the day, I: '
        if self.stopped:
            return False
        result += str(self.current_state)
        if 'finished homework' and 'volunteered' in self.characteristics:
            result += "\nCONGRATULATE ME. It was a productive day"
        print(result)
        return result

    def choose(self):
        return random.choice(self.current_state.possible_to_go)

    def __str__(self):
        return self.current_state.name

    def __repr__(self):
        result = "Now I "
        
    @work
    def change(self):
        """
        Moods: am tired, am energetic, studied, finished homework, volunteered, messy, hungry
        """
        while True:
            action = yield
            what_if = random.uniform(0, 1)
            if what_if >= 0.15:
                if action == 'sleep':
                    self.current_state = self.sleep
                    if "am tired" in self.characteristics:
                        self.delete_state('am tired')
                    else:
                        self.add_state("am energetic")
                elif action == 'study':
                    self.current_state = self.study
                    if self.characteristics.count('studied') >= 3:
                        self.add_state("finished homework")
                    else:
                        self.add_state("studied")
                elif action == 'walk':
                    self.current_state = self.walk
                    if 'hungry' not in self.characteristics:
                        self.add_state('hungry')
                elif action == 'eat':
                    self.current_state = self.eat
                    if 'hungry' in self.characteristics:
                        self.delete_state('hungry')
                elif action == 'volunteer':
                    self.current_state = self.volunteer
                    if self.characteristics.count('did some volunteering') >= 3:
                        self.add_state("volunteered")
                    else:
                        self.add_state("did some volunteering")
                elif action == 'wash':
                    self.current_state = self.wash
                    if 'messy' in self.characteristics:
                        self.delete_state('messy')
                    else:
                        self.add_state('energetic')
                elif action == 'relax':
                    self.current_state = self.relax
                    if 'messy' not in self.characteristics:
                        self.add_state('messy')
                else:
                    break
            else:
                print(f"I wanted to " + action + ", but something stopped me.")
                self.current_state = self.current_state


def start_your_day():
    simulator = Day(['am energetic', 'messy', 'hungry'])
    for hour in range(24):
        action = simulator.choose()
        simulator.send(action)
        print(f"Hour {hour}: I chose to " + str(simulator))
    return simulator.finite()


if __name__ == "__main__":
    start_your_day()