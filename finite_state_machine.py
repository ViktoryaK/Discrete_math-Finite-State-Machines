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


class Day:
    def __init__(self, characteristics=None):
        self.study = State('study', ["walk", "eat", 'sleep', 'relax'])
        self.walk = State("walk", ["study", "volunteer"])
        self.eat = State("eat", ["relax", "walk"])
        self.volunteer = State("volunteer", ["walk", "study"])
        self.wash = State("wash", ["study", "eat"])
        self.relax = State("relax", ["study", "volunteer", "eat"])
        self.sleep = State("sleep", ["eat", "wash", "study"])
        self.death = State("die", ['die', 'die'])
        self.productivity = 0
        if not characteristics:
            self.characteristics = []
        else:
            self.characteristics = characteristics
        self.current_state = self.sleep
        self.stopped = False

    def add_characteristic(self, characteristic):
        self.characteristics.append(characteristic)

    def delete_characteristic(self, characteristic):
        self.characteristics.remove(characteristic)

    def send(self, action):
        try:
            self.change().send(action)
        except StopIteration:
            self.stopped = True

    def finite(self):
        print("SUMMARY")
        if self.stopped:
            return False
        # print(self.productivity)
        if self.productivity >= 8:
            result = "CONGRATULATE ME. It was a productive day"
        else:
            result = "The day was not productive at all. Hope for tomorrow to be better."
        print(result)
        return result

    def die(self, wake, hour):
        if hour > wake:
            possible_deaths = ["Oh, too bad, it looks like I died from the car incident...", "Yes! It happened! I finally died from depression...", "I WILL RESURRECT AND KILL ALL THE RUSSIANS"]
        else:
            possible_deaths = ["I didn't woke up from the Air Alert and a missile striked and I died...", "Oh, it looks like I was ill and died from the illness in the sleep...", "My roommate killed me. That's all."]
        print("Death = True")
        print(random.choice(possible_deaths))
        return True



    def choose(self):
        return random.choice(self.current_state.possible_to_go)

    def __str__(self):
        return self.current_state.name

    def wake_up(self, hour, wake):
        if wake == hour:
            print(f"Hour {hour}")
            if wake <= 6:
                print("I woke up way too early in the morning mostly because of an Air Allert.")
                self.add_characteristic("tired")
            elif wake <= 8:
                print("I woke up perfectly in time and I am feeling fresh this morning.")
                self.add_characteristic("energetic")
            else:
                print("I overslept and skipped my morning class...")
                self.add_characteristic("tired")
                self.productivity -= 1
            return True
        elif hour < wake:
            print("Zzzzz....")
            return False
        else:
            return True


        
    @work
    def change(self):
        while True:
            action = yield
            what_if = random.uniform(0, 1)
            if what_if >= 0.15:
                if action == 'sleep':
                    self.current_state = self.sleep
                    if "tired" in self.characteristics:
                        self.delete_characteristic('tired')
                    else:
                        self.add_characteristic("energetic")
                elif action == 'study':
                    self.current_state = self.study
                    self.productivity += 1
                elif action == 'walk':
                    self.current_state = self.walk
                    if 'hungry' not in self.characteristics:
                        self.add_characteristic('hungry')
                elif action == 'eat':
                    self.current_state = self.eat
                    if 'hungry' in self.characteristics:
                        self.delete_characteristic('hungry')
                elif action == 'volunteer':
                    self.current_state = self.volunteer
                    self.productivity += 1
                elif action == 'wash':
                    self.current_state = self.wash
                    if 'messy' in self.characteristics:
                        self.delete_characteristic('messy')
                    else:
                        self.add_characteristic('energetic')
                elif action == 'relax':
                    self.current_state = self.relax
                    if 'messy' not in self.characteristics:
                        self.add_characteristic('messy')
                    if 'tired' in self.characteristics:
                        self.delete_characteristic('tired')
                elif action == "die":
                    self.current_state = self.death
                else:
                    break
            else:
                print(f"I wanted to " + action + ", but something stopped me.")
                self.current_state = self.current_state


def start_your_day():
    simulator = Day(['messy', 'hungry'])
    wake = random.randint(0, 10)
    u = None
    for hour in range(24):
        what_if = random.uniform(0, 1)
        if what_if <= 0.009:
            simulator.send("die")
            u = simulator.die(wake, hour)
        if u:
            break
        if simulator.wake_up(hour, wake):
            action = simulator.choose()
            simulator.send(action)
            print(f"Hour {hour}: I chose to " + str(simulator))
            print("Right now i am " + " and ".join(simulator.characteristics))
    if not u:
        return simulator.finite()


if __name__ == "__main__":
    start_your_day()