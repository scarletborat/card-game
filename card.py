class Card:
    def __init__(self, suit, value) -> None:
        self.suit = suit
        self.value = value
    
    def get_value(self) -> int:
        return self.value
    
    def get_suit(self) -> str:
        return self.suit
    