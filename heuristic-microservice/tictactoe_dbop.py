from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, null, Integer, String, JSON, DateTime
# from sqlalchemy.dialects.sqlite import JSON
from datetime import date
import logging
import sys
# from sqlalchemy import cast, type_coerce

Base = declarative_base()


class TicTacToeDbOp:
    engine = create_engine('sqlite:///tic-tac-toe.db', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    def __init__(self):
        Base.metadata.create_all(self.engine)

    def write(self, the_state, the_winner):
        try:
            game_data = GameState(the_state, the_winner)
            self.session.add(game_data)
            self.session.commit()
        except:
            logging.error('TicTacToeDbOp write() error: ', sys.exc_info()[0])
        return

    def close(self):
        self.session.close()


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

