import pickle
import os
import settings as s

def load(number=0):
    print("Loading")
    name = f"{s.SCRIPT_DIR}/{str(number)}/save.pkl"
    with open(name, 'rb') as file:
        data = pickle.load(file)
    name = f"{s.SCRIPT_DIR}/{str(number)}/savec.pkl"
    with open(name, 'rb') as file:
        data2 = pickle.load(file)
    return data, data2

def save(grid, crack_grid, number=0):
    print("saving")
    if not(os.path.exists(f"{s.SCRIPT_DIR}/{str(number)}")):
        os.makedirs(f"{s.SCRIPT_DIR}/{str(number)}")

    name = f"{s.SCRIPT_DIR}/{str(number)}/save.pkl"
    with open(name, 'wb') as file:
        pickle.dump(grid, file)
    name = f"{s.SCRIPT_DIR}/{str(number)}/savec.pkl"
    with open(name, 'wb') as file:
        pickle.dump(crack_grid, file)