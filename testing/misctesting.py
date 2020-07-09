import multiprocessing as m
import time

def f(x):
    return hash(x*x)

def g(x):
    return hash(x^x)

if __name__ == '__main__':
    print("Number of cpu : ", m.cpu_count())
    for y in range(10):
        if y:
            with m.Pool(y) as p:
                start = time.time()
                for x in range(10000):
                    p.map(f, range(50000))
                    p.map(g, range(50000))
        else:
            start = time.time()
            for x in range(10000):
                list(map(f, range(50000)))
                list(map(g, range(50000)))
        print(y, time.time() - start)
