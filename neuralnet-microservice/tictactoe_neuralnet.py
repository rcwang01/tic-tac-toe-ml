import keras
from keras.models import Sequential
from keras.layers import Dense
import numpy
# import os


def start_learning(csv_file):
    ml = TicTacToeLearning()
    ml.start(csv_file)
    ml.save_model()
    ml.save_weight()


class TicTacToeLearning:
    net_model = Sequential()
    file_base = ''

    def __init__(self):
        return

    def start(self, csv_file):
        self.file_base = csv_file
        numpy.random.seed(7)
        game_states = numpy.loadtxt(csv_file+'.csv', delimiter=',')
        # expected input and output for neural net
        state_input = game_states[:, 0:9]
        state_output = keras.utils.to_categorical(numpy.rint((game_states[:, 9]*10)-1), num_classes=10)

        self.net_model.add(Dense(15, input_dim=9, activation='relu'))
        self.net_model.add(Dense(9, activation='relu'))
        self.net_model.add(Dense(10, activation='sigmoid'))
        self.net_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        # Fit the model
        self.net_model.fit(state_input, state_output, epochs=100, batch_size=500)
        # evaluate the model
        scores = self.net_model.evaluate(state_input, state_output)
        print("\n%s: %.2f%%" % (self.net_model.metrics_names[1], scores[1]*100))

    def save_model(self):
        model_json = self.net_model.to_json()
        with open(self.file_base + '-model.json', 'w') as json_file:
            json_file.write(model_json)

    def save_weight(self):
        self.net_model.save_weights(self.file_base + '-weight.h5')

    def __del__(self):
        keras.backend.clear_session()


if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2:
        start_learning(sys.argv[1])
    elif len(sys.argv) == 1:
        start_learning('tic-tac-toe-x')
