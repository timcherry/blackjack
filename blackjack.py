#!/usr/bin/env python

import web
import json
import random

urls = (
    '/(.*)','MainRequestHandler'
)
app = web.application(urls, globals())

class MainRequestHandler:
    current_games = {}
    def GET(self, name):
        try:
            (action, user) = name.split("/") 
            assert (user and action), "Invalid Request"
            if user not in self.current_games:
                self.current_games[user] = Blackjack() 
            return self.current_games[user].handle_action(action)            
        except Exception as e:
            return self.handle_error(e)
    
    def handle_error(self,error):
        return json.dumps({"error":str(error)})

class Blackjack:
    def __init__(self,):
        self.reset_state()        

    def reset_state(self,):
        self.deck = None
        self.player = None
        self.dealer = None 

    def handle_action(self, action):
        if action == "deal": return self.deal()
        elif action == "hit": return self.hit()
        elif action == "stand": return self.stand()
        else: raise Exception("Invalid action.") 

    def deal(self):
        self.deck = Deck()
        self.player = BasePlayer()
        self.dealer = Dealer(self.deck)
        self.player.cards = self.deck.deal(2)
        self.dealer.cards = self.deck.deal(1)
        return self.return_state()

    def hit(self):
        assert self.deck, "No deck present. Try dealing first."
        self.player.cards.extend(self.deck.deal(1))
        return self.return_state()
 
    def stand(self):
        assert self.deck, "No deck present. Try dealing first."
        self.dealer.play()
        return self.return_state(player_stand=True)

    def declare_winner(self,):
        player_state, dealer_state = self.player.get_state(), self.dealer.get_state()
        if player_state == dealer_state:
            return ("Push","Push")
        elif player_state == "Busted":
            return ("Loser", "Winner")
        elif player_state == "Blackjack":
            return ("Winner", "Loser")
        elif dealer_state == "Busted":
            return ("Winner", "Loser")
        elif dealer_state == "Blackjack":
            return ("Loser", "Winner")
        elif player_state > dealer_state:
            return ("Winner", "Loser")
        else:
            return ("Loser","Winner")

    def is_game_over(self,):
        player_state = self.player.get_state()
        return (player_state == "Busted" or player_state == "Blackjack")

    def return_state(self, player_stand=False):
        game_over = False
        if self.is_game_over() or player_stand:
            (player_state, dealer_state) = self.declare_winner()
            game_over = True
        else:
            (player_state, dealer_state) = self.player.get_state(), self.dealer.get_state()
        game_state = {
            "player_cards"  : self.player.cards,
            "dealer_cards"  : self.dealer.cards,
            "player_state"  : player_state,
            "dealer_state"  : dealer_state,
        }
        if game_over:
            self.reset_state()
        return json.dumps(game_state)

class BasePlayer():
    def __init__(self,):
        self.cards = [] 

    def get_card_val(self, card):
        num = card[0]
        if num == "Ace": return 11
        elif num in ("King","Queen","Jack"): return 10
        else: return num

    def count_aces(self,):
        aces = 0
        for card in self.cards:
            if "Ace" in card: aces += 1
        return aces

    def sum_cards(self,):
        card_sum = sum([self.get_card_val(card) for card in self.cards])
        for x in range(self.count_aces()):
            if card_sum <= 21:
                break
            card_sum -= 10
        return card_sum

    def get_state(self,):
        player_sum = self.sum_cards()  
        if player_sum == 21:
            return "Blackjack" 
        if player_sum < 21:
            return player_sum 
        if player_sum > 21:
            return "Busted" 

class Dealer(BasePlayer):
    def __init__(self, deck):
        BasePlayer.__init__(self)
        self.deck = deck

    def play(self,):
        self.cards.extend(self.deck.deal(1))
        while self.sum_cards() < 17: 
            self.cards.extend(self.deck.deal(1))
 
class Deck:
    def __init__(self,):
        self.cards = [(num,suit) for num in range(2,11) + ["Ace","King","Queen","Jack"] 
            for suit in ['Spade', 'Heart', 'Club', 'Diamond']]
        random.shuffle(self.cards)

    def deal(self, count=0):
        assert len(self.cards) > count, "Too few cards to deal."
        return [self.cards.pop() for x in range(count)]

if __name__ == "__main__":
    app.run()
