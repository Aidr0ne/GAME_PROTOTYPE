import pickle

#TODO FIX ME NOW

def load(number=0):
    print("Loading")
    name = f"{str(number)}/save.pkl"
    with open(name, 'rb') as file:
        data = pickle.load(file)
    name = f"{str(number)}/savec.pkl"
    with open(name, 'rb') as file:
        data2 = pickle.load(file)
    return data, data2

def save(grid, crack_grid, number=0):
    print("saving")
    name = f"{str(number)}/save.pkl"
    with open(name, 'wb') as file:
        pickle.dump(grid, file)
    name = f"{str(number)}/savec.pkl"
    with open(name, 'wb') as file:
        pickle.dump(crack_grid, file)