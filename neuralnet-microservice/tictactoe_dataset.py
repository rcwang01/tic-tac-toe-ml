from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, null, Integer, String, JSON, DateTime
# -------------------------------------------
# TODO: Research why JSON db data type not working
# from sqlalchemy.dialects.sqlite import JSON
# -------------------------------------------
from datetime import date
import logging
import json
import sys

input_template = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.00]
winner_x_sequence = [1, 3, 5, 7, 9]
winner_o_sequence = [2, 4, 6, 8]
Base = declarative_base()
engine = create_engine('sqlite:///tic-tac-toe.db', echo=False)
Session = sessionmaker(bind=engine)


def  convert_to_neural_input(winner, begin_id, end_id):
    Base.metadata.create_all(engine)
    session = Session()
    counter = 0

    try:
        # Here game_state is equivalent to game_data variable in
        # heuristic_microservice
        game_states = session.query(GameState) \
            .filter(GameState.winner == winner \
                    , GameState.id >= begin_id \
                    , GameState.id <= end_id) \
            .all()
        for game_state in game_states:
            the_state = json.loads(str(game_state.state))
            step_count = len(the_state) - 1
            winner_sequence = []
            if winner == 'X':
                winner_sequence = winner_x_sequence.copy()
            elif winner == 'O':
                winner_sequence = winner_o_sequence.copy()
            for index in range(len(winner_sequence)):
                the_input = input_template.copy()
                the_sequence = winner_sequence[index]
                for sub_index in range(the_sequence):
                    position_pair = the_state.get(sub_index+1)
                    if position_pair is None:
                        break
                    the_input[sub_index] = position_pair[0]
                the_input[len(input_template)-1] = round(the_sequence/step_count, 2)
                print('Row ID ' + str(begin_id+index) + ' convert to ' + str(the_input))
            counter += 1

    except:
        logging.error('convert_to_neural_input query() error: ', sys.exc_info()[0])

    session.close()
    print(str(counter) + ' data set has been converted.')


class GameState(Base):
    __tablename__ = 'game_state'
    id = Column(Integer, primary_key=True)
    # state = Column(JSON)
    state = Column(String)
    winner = Column(String(1))
    create_datetime = Column(DateTime)

    def __init__(self, the_state, the_winner):
        self.state = the_state
        self.winner = the_winner
        self.create_datetime = date.today()


if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 4:
        convert_to_neural_input(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    elif len(sys.argv) == 3:
        convert_to_neural_input(sys.argv[1], int(sys.argv[2]), 999999)
    else:
        print('Error: Please enter at least two argument')
