import dill
import os

file = "../test.obj"

if __name__ == "__main__":
    if os.path.exists(file):
        print("found")
        with open(file, "rb") as f:
            data = dill.load(f)
        print(type(data))
    else:
        print("not found")
