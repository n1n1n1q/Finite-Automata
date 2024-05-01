"""
FSM
"""

import time
import random


class PassAwayException(Exception):
    """
    Pass awa exception
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def to_generator(func):
    """
    ...
    """

    def wrapper(*args, **kwargs):
        f = func(*args, **kwargs)
        next(f)
        return f

    return wrapper


class FSM:
    """
    FSM class
    """

    STUDY_HOURS = [9, 10, 11, 12, 13] + [17, 18, 19, 20, 21] + [0, 1, 2, 3]
    OVERSTUDY_HOURS = [15, 23, 5]

    def __init__(self, extended: bool = False) -> None:
        self.extended = extended
        self.energy_level = 1
        self.hunger = 8
        self.sanity = 10
        self.study_streak = 0
        self.current_state = None
        self.set_up()
        self.start()

    def set_up(self):
        """
        Set the FSM's states up
        """
        self.state_sleep = self._sleep()
        self.state_study = self._study()
        self.state_eat = self._eat()
        self.state_relax = self._relax()
        self.state_coffee = self._coffee_break()
        self.current_state = self.state_sleep

    def send_input(self, hour):
        """
        ...
        """
        self.current_state.send(hour)
        if self.sanity <= 0:
            print("You went crazy")
            raise PassAwayException("you died lol")
        if self.hunger <= 0:
            print("You starved to death")
            raise PassAwayException("you died lol")

    @to_generator
    def _sleep(self):
        """
        Sleep
        """
        while True:
            hour = yield
            dice = random.random()
            self.__debug(hour, "Sleep")
            if hour == 7 and dice <= 0.8:
                print("Wakey wakey! It's time for uni")
                self.current_state = self.state_eat
            elif hour == 8:
                print("Oh no! You missed your alarm")
                self.sanity -= 1
                self.hunger -= 1
                self.current_state = self.state_study
            else:
                print("Zzz.....")
                self.energy_level += 1
                self.hunger -= 0.5

    @to_generator
    def _eat(self):
        """
        Eat
        """
        while True:
            hour = yield
            dice = random.random()
            self.__debug(hour, "Eat / Cook")
            if dice > 0.75:
                print("You messed your cooking up, now you're in despair")
                self.current_state = self.state_relax
            elif hour == 8:
                print("You had a proper breakfast")
                self.hunger += 2.5
                self.energy_level += 2
                self.sanity+=1
                self.current_state = self.state_study
            elif hour == 15:
                print("You cooked for dinner the best pasta in your life!")
                self.hunger+=4
                self.energy_level+=4
                self.sanity+=2
                self.current_state = self.state_relax
            else:
                print("You had a snack")
                self.hunger+=2
                self.energy_level+=1
                self.current_state = self.state_relax

    @to_generator
    def _study(self):
        """
        Study
        """
        while True:
            hour = yield
            dice = random.random()
            self.__debug(hour, "Study")
            if dice > 0.75 and hour + 1 in self.STUDY_HOURS:
                print("It's time for coffee!")
                self.current_state = self.state_coffee
            elif hour in self.OVERSTUDY_HOURS and dice > 0.6:
                print("You forgot about exhaustion and continued studying")
                self.energy_level -= 1
                self.hunger -= 0.5
                self.sanity -= 1
                self.study_streak += 1
            elif hour in self.STUDY_HOURS:
                print("Studying...")
                self.study_streak += 1
                self.energy_level -= 1
                self.hunger -= 0.5
            elif self.is_exhausted(hour):
                print("You felt so exhausted so you went sleeping")
                self.study_streak = 0
                self.current_state = self.state_sleep
            else:
                print("You are going to have a meal")
                print(hour)
                self.study_streak = 0
                self.current_state = self.state_eat

    @to_generator
    def _relax(self):
        """
        Relax break
        """
        while True:
            hour = yield
            self.__debug(hour, "Relax")
            print("Relax time!")
            self.study_streak = 0
            self.sanity += 2
            self.hunger -= 1
            self.current_state = self.state_study

    @to_generator
    def _coffee_break(self):
        """
        Break for a cup of coffee
        """
        while True:
            hour = yield
            dice = random.random()
            self.__debug(hour, "Coffee")
            if dice < 0.2:
                print("The machine is broken, you couldn't get coffee")
                self.energy_level -= 0.5
                self.sanity -= 0.5
                self.current_state = self.state_study
            elif dice > 0.7:
                print("The coffee is so good!")
                self.energy_level += 2
                self.sanity += 0.5
                self.current_state = self.state_study
            else:
                print("Sipping some coffee")
                self.energy_level += 1
                self.current_state = self.state_study

    def start(self):
        """
        Start FSM loop
        """
        curr = 0
        while 1:
            try:
                self.send_input(curr % 24)
            except PassAwayException:
                break
            time.sleep(0.1)
            curr += 1

    def is_exhausted(self, hour):
        """
        Is exhausted
        """
        return hour in range(0, 4) and self.energy_level > 3

    def __debug(self, hour, state):
        if self.extended:
            print(f"""
=============================
    CURRENT HOUR = {hour}
   CURRENT STATE = {state}
=============================
""")

if __name__ == "__main__":
    automata = FSM(True)
