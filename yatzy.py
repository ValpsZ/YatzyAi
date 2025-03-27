from __future__ import annotations
import random

MAX_SCORES = {
    "1": 5,
    "2": 10,
    "3": 15,
    "4": 20,
    "5": 25,
    "6": 30,
    "pair": 12,
    "two_pairs": 22,
    "three_of_a_kind": 18,
    "four_of_a_kind": 24,
    "full_house": 28,
    "small_straight": 15,
    "large_straight": 20,
    "chance": 30,
    "yatzy": 50  
}

class GameState:
    def __init__(self,game:Game):
        self.scores = game.scores
        self.dice = game.dice

class Game:
    def __init__(self):
        self.scores = {
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0,
            "5": 0,
            "6": 0,
            "bonus": None,
            "pair": 0,
            "two_pairs": 0,
            "three_of_a_kind": 0,
            "four_of_a_kind": 0,
            "full_house": 0,
            "small_straight": 0,
            "large_straight": 0,
            "chance": 0,
            "yatzy": 0
        }

        self.dice = [None,None,None,None,None]
        self.rollDice([i for i in range(5)])
    
    def saveState(self) -> GameState:
        return GameState(self)
    
    def loadState(self,state:GameState):
        self.dice = state.dice
        self.scores = state.scores
    
    def getScore(self) -> int:
        return sum(score for score in self.scores.values() if score != None)

    def rollDice(self,diceNr:list[int]=[0,1,2,3,4]) -> None:
        for dice in diceNr:
            self.dice[dice] = random.randint(1, 6)
        self.dice = sorted(self.dice)
    
    def getPairs(self) -> list[int]:
        pairs = []
        for i in range(1,7):
            if self.dice.count(i) > 1:
                pairs.append(i)
        return pairs
    
    def getThreeOfAKind(self) -> list[int]:
        threeOfAKind = []
        for i in range(1,7):
            if self.dice.count(i) > 2:
                threeOfAKind.append(i)
        return threeOfAKind

    def getCombinations(self, numbers:list[int]) -> list[tuple[int,int]]:
        combinations:list[tuple[int,int]] = []
        for i in range(len(numbers)):
            for j in range(i+1,len(numbers)):
                if (numbers[j],numbers[i]) not in combinations:
                    combinations.append((numbers[i],numbers[j]))
        return combinations

    def getPossibleOptions(self) -> dict[str,list[int]]:
        options:dict[str,list[int]] = {}
        # Numbers
        for i in range(1,7):
            ammount = self.dice.count(i)
            if ammount > 0 and self.scores[str(i)] == 0:
                options[str(i)] = [i * ammount]
        
        # Pair
        if self.scores["pair"] == 0:
            for nr in self.getPairs():
                if "pair" not in options: options["pair"] = []
                options["pair"].append(nr * 2)
        
        # Two pairs
        if self.scores["two_pairs"] == 0:
            if len(set(self.getPairs())) > 1:
                if "two_pairs" not in options: options["two_pairs"] = []
                for combination in self.getCombinations(self.getPairs()):
                    options["two_pairs"].append(combination[0]*2+combination[1]*2)
        
        # Three of a kind
        if self.scores["three_of_a_kind"] == 0:
            for nr in self.getThreeOfAKind():
                if "three_of_a_kind" not in options: options["three_of_a_kind"] = []
                options["three_of_a_kind"].append(nr*3)

        # Four of a kind
        if self.scores["four_of_a_kind"] == 0:
            for i in range(1,7):
                if self.dice.count(i) > 3:
                    if "four_of_a_kind" not in options: options["four_of_a_kind"] = []
                    options["four_of_a_kind"].append(i*4)
        
        # Full house
        if self.scores["full_house"] == 0:
            # If there is a three of a kind, there is already a pair so we need to check if there is more than 1 pair
            if len(self.getThreeOfAKind()) > 0 and len(self.getPairs()) > 1:
                options["full_house"] = [sum(self.dice)]
        
        # Small straight
        if self.scores["small_straight"] == 0:
            if sorted(self.dice) == [1,2,3,4,5]:
                options["small_straight"] = [15]
        
        # Large straight
        if self.scores["large_straight"] == 0:
            if sorted(self.dice) == [2,3,4,5,6]:
                options["large_straight"] = [20]
        
        # Chance
        if self.scores["chance"] == 0:
            options["chance"] = [sum(self.dice)]

        # Yatzy
        if self.scores["yatzy"] == 0:
            if len(set(self.dice)) == 1:
                options["yatzy"] = [50]

        return options
    
    def putScore(self,option:str,value:int) -> None:
        if option not in self.getPossibleOptions():
            print("Option not possible")
            return
        if option not in self.scores:
            print("Option not found")
            return
        self.scores[option] = value
    
    def calcTop(self) -> int:
        return sum(self.scores[str(i)] for i in range(1, 7) if self.scores[str(i)] != None)
    
    def isBonusPossible(self) -> bool:
        return self.calcTop() + sum(MAX_SCORES[i] for i in ["1", "2", "3", "4", "5", "6"] if self.scores[i] != None)