Feature: Minimax algorithm for Tic-Tac-Toe game

  Scenario: Start a new game as MAX
    Given the game board is blank
    When the machine makes a move first as an X
    Then the machine will performs AI reasoning and make the first move

  Scenario: Start a new game as an O
    Given the opponent makes a move first as an X
    When the machine identifies the move from the opponent
    Then the machine will performs AI reasoning and make the next move

  Scenario: Determine the next move after the game has started
    Given the opponent makes a move at any time
    When the machine identifies the move from the opponent
    Then the machine will performs AI reasoning and make the next move

  Scenario: Determine game over
    Given there are at least three Xs or three Os on the game board
    When whoever has completed a move
    Then the machine checks the game board to determine a winner
    And yield X or O as the winner
