from KarelInput import KarelInputCase, Orientation, EvalFlags, WallFlags, Point
from KarelOutput import KarelOutputCase


def writeCase(A, B, name):
    case = KarelInputCase(
        beeperBag=-1,
        evaluationFlags=EvalFlags.POSITION
    )

    case.placeBeepers(Point(1, 1), A)
    case.placeBeepers(Point(2, 1), B)
    case.dumpCell(Point(1, 1))
    case.dumpCell(Point(2, 1))

    case.write(f"{name}.in", True)

    output = KarelOutputCase()

    output.setBeepers(Point(1, 1), A)
    output.setBeepers(Point(2, 1), B)
    output.setPosition(Point(1,1) if A > B else Point(2,1))
    output.write(f"{name}.out", format=True, input=case)


numbers=[
    (8,12),
    (1,2),
    (10,40),
    (100,1),
    (100,99)
    ]
for i, (A, B) in enumerate(numbers):
    writeCase(A, B, f"bin/c{i}.a")
    writeCase(B, A, f"bin/c{i}.b")
