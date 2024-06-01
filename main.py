from KarelInput import KarelInputCase, Orientation, EvalFlags, WallFlags, Point
from KarelOutput import KarelOutputCase
import random


def writeCase(n, name):
    case = KarelInputCase(
        beeperBag=-1,
        start_x=1,
        start_y=1,
        evaluationFlags= EvalFlags.ALLBEEPERS
    )

    


    output = KarelOutputCase()

    case.write(f"{name}.in", True)
    output.write(f"{name}.out", format=True, input=case)


sizes = [3, 5, 8, 9, 13, 
        99, 55, 34, 59, 80, 
        10, 22, 14, 60, 29, 
        40, 89, 79, 89, 7]

# for i, n in enumerate(sizes):
#     writeCase(n, f"./bin/case{i}")