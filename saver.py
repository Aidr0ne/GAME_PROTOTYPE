import pickle

def load(number=0):
    print("Loading")
    name = "save" + str(number) + ".pkl"
    with open(name, 'rb') as file:
        data = pickle.load(file)
    name = "save" + str(number) + "c.pkl"
    with open(name, 'rb') as file:
        data2 = pickle.load(file)
    return data, data2

def save(grid, crack_grid, number=0):
    print("saving")
    name = "save" + str(number) + ".pkl"
    with open(name, 'wb') as file:
        pickle.dump(grid, file)
    name = "save" + str(number) + "c.pkl"
    with open(name, 'wb') as file:
        pickle.dump(crack_grid, file)