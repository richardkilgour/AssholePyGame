from asshole.cards.Meld import Meld
from asshole.player.AbstractPlayer import AbstractPlayer, possible_plays
from asshole.player.PlayerSimple import PlayerSimple


class PyGamePlayer(PlayerSimple):
    def __init__(self, name):
        AbstractPlayer.__init__(self, name)
        # NextAction can be None (no action) or a list or cards to play (empty list = pass)
        self.NextAction = None

    def send_keypress(self, key):
        self.NextAction = key

    def send_card_click(self, clicked_card):
        """Find the highest value card that was clicked (in case many cards are clicked)"""
        # If this is a card in the hand, play it
        if clicked_card == 'PASS':
            self.NextAction = 'PASS'
        if self.NextAction == 'PASS':
            return
        if self.NextAction and self.NextAction.get_index() > clicked_card.get_index():
            # Only if it's higher than all the existing 'action' cards, replace them
            print(f"Click on {clicked_card} ignored due to {self.NextAction}")
        else:
            print(f"Clicked on {clicked_card} replaces {self.NextAction}")
            self.NextAction = clicked_card

    def show_player(self, i):
        pass

    def play(self):
        """
        Process an action set by another thread
        Return a meld (set of cards) if a valid card was clicked
        Return a pass (empty Meld) if the clicked card is an empty set
        Fall through if no action is selected yet (return noop '␆')
        """
        if self.NextAction is None:
            return '␆'
        if self.NextAction == 'PASS':
            # Reset the last action
            self.NextAction = None
            # Return null meld ('pass')
            return Meld()

        # Check if it's valid
        selection = possible_plays(self._hand, self.target_meld, self.name)

        # Last option is Pass, so ignore it
        for s in selection[:-1]:
            # Logic for multiple selections relies on highest card not being on lower combos
            if self.NextAction.get_index() == s.cards[-1].get_index():
                self.NextAction = None
                return s
        print(f'INVALID CLICK; {self.NextAction} is not better than {self.target_meld}')
        self.NextAction = None
        return '␆'
