Dependencies
==============
python web.py

    $sudo easy_install web.py

Running
========

    $python blackjack.py
    
API
====

Each of the below gamplay requests will return a json object with the following information:

        {"dealer_state": 7, 
        "player_cards": [["Ace", "Club"], [3, "Diamond"]], 
        "player_state": 14, 
        "dealer_cards": [[7, "Club"]]}

Once the game is declared over. The following json object is returned:

        {"dealer_state": "Loser", 
        "player_cards": [["Ace", "Club"], [3, "Diamond"]], 
        "player_state": "Winner", 
        "dealer_cards": [[7, "Club"], [8, "Heart"], [7, "Spade"]]}

In the event of an error the following is returned:

        {"error": <ERROR DESCRIPTION>}

Gameplay
==========

**Deal**

The game starts by calling deal. Deal can be called at any point to start a new hand.

      $curl localhost:8080/deal/<your_name>

**Hit**

After dealing, the player can call hit till he either hits blackjack, or busts.

      $curl localhost:8080/hit/<your_name>
      
**Stand**

After dealing, the player can choose to stand at any point. Once the player stands, the dealer will draw cards till he busts or reaches a hand worth more than 17. A winner is determined and results are returned.

      $curl localhost:8080/stand/<your_name>

