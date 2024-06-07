import pickle
import os
from lib.robot import Robot


def loader(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            try:
                r = pickle.load(file)
                print(f'Object loaded from {filename}')
            except (pickle.PickleError, EOFError) as e:
                print(f'Error loading object: {e}')
                r = None
    else:
        r = None

    if r is None:
        r = Robot()
        print('New object created')

    return r


def saver(filename, obj):
    with open(filename, 'wb') as file:
        pickle.dump(obj, file)
        print(f'Object saved to {filename}')


def main():
    f = "robot.pkl"
    robot = loader(f)
    robot.auto_move(10)
    saver(f, robot)


if __name__ == "__main__":
    main()
