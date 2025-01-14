from tensorflow import keras
from tensorflow.keras import layers
from Savery import *

import math


def create_network():
    print("\n## Create network model:")
    input_layer = keras.Input(shape=(32,), name='checkers_board')

    hidden_layer_1 = layers.Dense(64, activation='relu', name='dense_1')(input_layer)
    hidden_layer_2 = layers.Dense(128, activation='relu', name='dense_2')(hidden_layer_1)
    hidden_layer_3 = layers.Dense(512, activation='relu', name='dense_3')(hidden_layer_2)
    hidden_layer_4 = layers.Dense(1024, activation='relu', name='dense_4')(hidden_layer_3)
    hidden_layer_5 = layers.Dense(512, activation='relu', name='dense_5')(hidden_layer_4)
    hidden_layer_6 = layers.Dense(128, activation='relu', name='dense_6')(hidden_layer_5)
    hidden_layer_7 = layers.Dense(64, activation='relu', name='dense_7')(hidden_layer_6)

    output_piece = layers.Dense(32, name='piece')(hidden_layer_7)

    model = keras.Model(
        inputs=[input_layer],
        outputs=[output_piece],
    )

    print("\n## Compile network:")
    model.compile(optimizer=keras.optimizers.RMSprop(),
                  loss=keras.losses.MeanSquaredError(),
                  metrics=[keras.metrics.MeanSquaredError()])

    model.summary()

    model.save("model_piece_3")
    print("end - out create_network")
    # keras.utils.plot_model(model, "my_first_model.png")
    # tf.keras.utils.plot_model(model, to_file="my_first_model.png", show_shapes=True)


# ----------------------------------------------------------------------------------------------------------------------
def fit_network():
    model = keras.models.load_model("model_piece_3")

    print("\n## Load and reshape input/output data:")
    sample = 16
    number_of_games = 16

    train_input = load_board(sample, number_of_games)
    train_input = train_input.astype('float32') / 5
    print("train_input ", train_input)
    print("shape ", train_input.shape)
    print()

    train_output_piece = load_piece(sample, number_of_games)
    train_output_piece = train_output_piece.astype('float32')
    print("train_output_piece ", train_output_piece)
    print("shape ", train_output_piece.shape)
    print()

    print('\n## Train the model on train_data')
    # history = model.fit(train_input,
    #                     y=[train_output_piece, train_output_move],
    #                     batch_size=32,
    #                     epochs=200,
    #                     validation_data=(validation_input, [validation_output_piece, validation_output_move]))
    history = model.fit(train_input,
                        y=train_output_piece,
                        batch_size=32,
                        epochs=40)

    print('\nhistory dict:', history.history)

    model.save("model_piece_3")
    print("end - out fit_network")
# ---------------------------------------------------------------------------------------------------------------------
def get_move_from_network(checkers):
    model = keras.models.load_model("model_piece_3")

    board_list = []

    for i in range(len(checkers.board)):
        for j in range(len(checkers.board[i])):

            if (i + j) % 2 == 0:
                continue

            element = checkers.board[i][j]
            if element == 'A':
                board_list.append(0)
            elif element == 'a':
                board_list.append(1)
            elif element == ' ':
                board_list.append(2)
            elif element == 'r':
                board_list.append(3)
            elif element == 'R':
                board_list.append(4)

    num_list = np.array(board_list)
    train_input = num_list.astype('float32') / 5

    train_input = np.reshape(train_input, (1, 32))
    # print("train_input ", type(train_input))
    # print(train_input.shape)
    # print(train_input)
    # print()

    predictions = model.predict(train_input)

    print("train_input ", type(predictions))
    # print("shape ", predictions.shape)
    print(predictions)
    # print(sum(predictions[0]) )
    # print()
    piece = np.argmax(predictions[0])
    print("sum 0 ", sum(predictions[0][0]))
    move = np.argmax(predictions[1])
    print("sum 1 ", sum(predictions[1][0]))
    print(piece, " ", move)

    for i in range(32):
        print(i, " ", predictions[1][0][i] * 100)

    x1 = math.floor(piece / 4)
    x2 = ((piece % 4) * 2 + 1) if x1 % 2 == 0 else ((piece % 4) * 2)
    y1 = math.floor(move / 4)
    y2 = ((move % 4) * 2 + 1) if y1 % 2 == 0 else ((move % 4) * 2)

    model.save("model_piece_3")

    return [[x1, x2], [y1, y2]]

def test_network():
    model = keras.models.load_model("model_piece_3")

    print("\n## Load and reshape input/output data:")
    sample = 1
    number_of_games = 1

    train_input = load_board(sample, number_of_games)
    train_input = train_input.astype('float32') / 5
    print("train_input ", train_input)
    print("shape ", train_input.shape)
    print()
    train_output_piece = load_piece(sample, number_of_games)
    train_output_piece = train_output_piece.astype('float32')
    print("train_output_piece ", train_output_piece)
    print("shape ", train_output_piece.shape)
    print()

    # # Оценим модель на тестовых данных, используя "evaluate"
    print('## Evaluate network:')
    results = model.evaluate(train_input, train_output_piece, batch_size=32)
    print('test loss, test acc:', results)

    print("train_input ", type(train_input[2:3]))
    print(train_input[2:3].shape)
    print(train_input[2:3])
    print()

    # Сгенерируем прогнозы (вероятности - выходные данные последнего слоя)
    # на новых данных с помощью "predict"
    print('\n# Генерируем прогнозы для 3 образцов')
    predictions = model.predict(train_input[2:3])
    print(predictions)
    print("predictions[0]", predictions[0])
    print()
    print(np.argmax(predictions[0]))
    # for i in range(len(predictions)):
    #     print("test_output ", train_output_piece[i], " pred ", np.argmax(predictions[i][0]))
    #     print("test_output ", train_output_move[i], " pred ", np.argmax(predictions[i][0]))

    model.save("model_piece_3")


if __name__ == "__main__":
    create_network()

    # model = keras.models.load_model("model_piece_3")
    # dot_img_file = '/tmp/model_1.png'
    # keras.utils.plot_model(model, to_file = dot_img_file, show_shapes = True)


    # fit_network()

    # test_network()

    # model = keras.models.load_model("model_piece_3")
    # model.summary()
