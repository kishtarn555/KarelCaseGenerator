from KarelInput import KarelInputCase, Orientation, EvalFlags, WallFlags, Point


case = KarelInputCase(
    width=30, 
    height=70, 
    beeperBag=14,
    start_x=1, 
    start_y=2, 
    orientation=Orientation.SOUTH,
    evaluationFlags=EvalFlags.BEEPERBAG | EvalFlags.ORIENTATION
    )

print(Orientation.SOUTH.value[0])

case.placeBeepers(Point(5,8), 10)

case.toggleWall(Point(3,4), WallFlags.ALL )
case.toggleWall(Point(4,4), WallFlags.ALL )
case.toggleWall(Point(5,4), WallFlags.ALL )
case.toggleWall(Point(5,3), WallFlags.ALL )

case.dumpCell(Point(5,3))


case.write("output.in", True)


