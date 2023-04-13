from typing import Dict, Tuple
import xml.etree.ElementTree as ET
from KarelUtil import *

class KarelInputCase:
    def __init__(
            self,
            *,
            width: int = 100,
            height: int = 100,
            beeperBag:int = 0,
            start_x:int = 1,
            start_y:int = 1,
            orientation: Orientation = Orientation.NORTH,
            evaluationFlags: int = 0
    ):
        self.width: int = width
        self.height:int = height
        self.beepers:int = beeperBag
        self.karel_x:int = start_x
        self.karel_y:int = start_y
        self.karel_orientation: Orientation = orientation
        self.karel_beepers: int = beeperBag

        self.beepers : Dict[Point: int] = {}
        self.evaluationFlags: int = evaluationFlags
        self.walls = [[0]*(height+1) for _ in range(width+1)]
        self.dumpCells =[[False]*(height+1) for _ in range(width+1)]

    def placeBeepers(self,coords: Point, ammount:int)-> None:
        self.beepers[coords] = ammount

    def placeWall(self, coords: Point, walls:int) -> None:
        if coords.x!=1 and (walls & WallFlags.LEFT):
            self.walls[coords.x][coords.y] |= WallFlags.LEFT
            self.walls[coords.x-1][coords.y] |= WallFlags.RIGHT

        if coords.y!=1 and (walls & WallFlags.DOWN):
            self.walls[coords.x][coords.y] |= WallFlags.DOWN
            self.walls[coords.x][coords.y-1] |= WallFlags.UP
            
        if coords.x!=self.width and (walls & WallFlags.RIGHT):
            self.walls[coords.x][coords.y] |= WallFlags.RIGHT
            self.walls[coords.x+1][coords.y] |= WallFlags.LEFT

        if coords.y!=self.height and (walls & WallFlags.UP):
            self.walls[coords.x][coords.y] |= WallFlags.UP
            self.walls[coords.x][coords.y+1] |= WallFlags.DOWN

    def removeWall(self, coords: Point, walls:int) -> None:
        if coords.x!=1 and (walls & WallFlags.LEFT):
            self.walls[coords.x][coords.y] &= ~WallFlags.LEFT
            self.walls[coords.x-1][coords.y] &= ~WallFlags.RIGHT

        if coords.y!=1 and (walls & WallFlags.DOWN):
            self.walls[coords.x][coords.y] &= ~WallFlags.DOWN
            self.walls[coords.x][coords.y-1] &= ~WallFlags.UP
            
        if coords.x!=self.width and (walls & WallFlags.RIGHT):
            self.walls[coords.x][coords.y] &= ~WallFlags.RIGHT
            self.walls[coords.x+1][coords.y] &= ~WallFlags.LEFT

        if coords.y!=self.height and (walls & WallFlags.UP):
            self.walls[coords.x][coords.y] &= ~WallFlags.UP
            self.walls[coords.x][coords.y+1] &= ~WallFlags.DOWN
            

    def toggleWall(self, coords: Point, walls:int) -> None:
        if coords.x!=1 and (walls & WallFlags.LEFT):
            self.walls[coords.x][coords.y] ^= WallFlags.LEFT
            self.walls[coords.x-1][coords.y] ^= WallFlags.RIGHT

        if coords.y!=1 and (walls & WallFlags.DOWN):
            self.walls[coords.x][coords.y] ^= WallFlags.DOWN
            self.walls[coords.x][coords.y-1] ^= WallFlags.UP
            
        if coords.x!=self.width and (walls & WallFlags.RIGHT):
            self.walls[coords.x][coords.y] ^= WallFlags.RIGHT
            self.walls[coords.x+1][coords.y] ^= WallFlags.LEFT

        if coords.y!=self.height and (walls & WallFlags.UP):
            self.walls[coords.x][coords.y] ^= WallFlags.UP
            self.walls[coords.x][coords.y+1] ^= WallFlags.DOWN
            
    def dumpCell(self, coords:Tuple[int,int])->None:
        self.dumpCells[coords.x][coords.y] = True
    
    def ignoreCell(self, coords:Tuple[int,int])->None:
        self.dumpCells[coords.x][coords.y] = False
    
    def ToggleDumpCell(self, coords:Tuple[int,int])->None:
        self.dumpCells[coords.x][coords.y] = not self.dumpCells[coords.x][coords.y]

    def toXML(self):
        ejecucion = ET.Element("ejecucion")

        condiciones = ET.SubElement(ejecucion, "condiciones") # <condiciones instruccionesMaximasAEjecutar="10000000" longitudStack="65000"></condiciones>
        condiciones.set("instruccionesMaximasAEjecutar", "10000000") # TODO: Add a setting for this
        condiciones.set("longitudStack", "65000") # TODO: Add a setting for this

        mundos = ET.SubElement(ejecucion, "mundos")

        self._buildWorldXML(mundos)

        programas = ET.SubElement(ejecucion,"programas")
        programas.set("tipoEjecucion", "CONTINUA")
        programas.set("intruccionesCambioContexto", "1") # NOTE: IDK WHAT THIS DOES
        programas.set("milisegundosParaPasoAutomatico", "0") # NOTE: IDK WHAT THIS DOES

        self._buildProgramXML(programas)

        return ET.ElementTree(ejecucion)
    
    def _buildWorldXML(self, mundos):        
        mundo = ET.SubElement(mundos, "mundo")
        mundo.set("nombre", "mundo_0")
        mundo.set("ancho", "mundo_0")
        mundo.set("alto", f"{self.height}")
        mundo.set("ancho", f"{self.width}")

        for coords, value in self.beepers.items():
            monton = ET.SubElement(mundo, "monton")
            monton.set("x", f"{coords.x}")
            monton.set("y", f"{coords.y}")
            monton.set("zumbadores", f"{value}")

        for x in range(1, self.width):
            for y in range(1, self.height+1):
                if (self.walls[x][y] & WallFlags.RIGHT)!=0:
                    pared = ET.SubElement(mundo, "pared")
                    pared.set("x1", f"{x}")
                    pared.set("y1", f"{y-1}")
                    pared.set("y2", f"{y}")

        
        for x in range(1, self.width+1):
            for y in range(1, self.height):
                if (self.walls[x][y] & WallFlags.UP)!=0:
                    pared = ET.SubElement(mundo, "pared")
                    pared.set("x1", f"{x-1}")
                    pared.set("y1", f"{y}")
                    pared.set("x2", f"{x}")

    
    def _buildProgramXML(self, programasNode):
        programa = ET.SubElement(programasNode, "programa")

        programa.set("nombre", "p1") # NOTE: idk
        programa.set("ruta","{$2$}") #NOTE: idk
        programa.set("mundoDeEjecucion","mundo_0") 
        programa.set("xKarel",f"{self.karel_x}") 
        programa.set("yKarel",f"{self.karel_y}") 

        
        programa.set(
            "direccionKarel", 
            f"{ORIENTATION_DECODE[self.karel_orientation.value[0]]}"
        ) 
        programa.set(
            "mochilaKarel", 
            f"{self.karel_beepers if self.karel_beepers != -1 else 'INFINITO'}"
            )
        
        def despliega(type:str):
            el = ET.SubElement(programa, "despliega")
            el.set("tipo", type)
            return el

        if (self.evaluationFlags & EvalFlags.POSITION):
            despliega("POSICION")
        if (self.evaluationFlags & EvalFlags.ORIENTATION):
            despliega("ORIENTACION")
        if (self.evaluationFlags & EvalFlags.BEEPERBAG):
            despliega("MOCHILA")
        if (self.evaluationFlags & EvalFlags.ALLBEEPERS):
            despliega("UNIVERSO")

        for x in range(1, self.width+1):
            for y in range(1, self.height+1):
                if self.dumpCells[x][y]:
                    dump = ET.SubElement(programa, "posicionDump")
                    dump.set("x", f"{x}")
                    dump.set("y", f"{y}")


    def write(self, path: str, format:bool = False):
        xml = self.toXML()
        if (format):
            ET.indent(xml, space="\t", level=0)
        xml.write(path)
