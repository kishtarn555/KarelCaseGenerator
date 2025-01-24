from typing import Dict, Optional, Tuple
import xml.etree.ElementTree as ET
from .KarelUtil import *
from dataclasses import dataclass
from .constants import TargetVersion
@dataclass(kw_only=True, frozen=True)
class ExecutionLimits:
    instruction_limit:int = 10_000_000
    stack_size:int = 65_000
    stack_memory:int = 65_000
    parameter_limit:int = 5
    move_limit:int = -1
    left_limit:int = -1
    leave_limit:int = -1
    pick_limit:int = -1




class KarelInputCase:
    def __init__(
            self,
            *,
            width: int = 100,
            height: int = 100,
            beeperBag:int = 0,
            start_x:int = 1,
            start_y:int = 1,
            limits:Optional[ExecutionLimits] = None,
            orientation: Orientation = Orientation.NORTH,
            evaluationFlags: int = 0,
            target_version: TargetVersion = "1.0"
    ):
        self.width: int = width
        self.height:int = height
        self.karel_x:int = start_x
        self.karel_y:int = start_y
        self.karel_orientation: Orientation = orientation
        self.karel_beepers: int = beeperBag
        self.limits: ExecutionLimits = ExecutionLimits()

        self.beepers : Dict[Point: int] = {}
        self.evaluationFlags: int = evaluationFlags
        self.walls = [[0]*(height+1) for _ in range(width+1)]
        self.dumpCells =[[False]*(height+1) for _ in range(width+1)]
        if limits is not None:
            self.limits = limits
        self.target_version = target_version

            

    def placeBeepers(self,coords: Point, amount:int)-> None:
        """Sets the number of beepers at a given."""
        self.beepers[coords] = amount

    def placeWall(self, coords: Point, walls:int) -> None:
        """At a cell, it adds walls, and it updates the corresponding neighbor.

        :param Point coords: Coordinates of the cell to place
        :param int walls: Wall byte mask to add.
        """
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
        """It removes the walls from a cell, and it's corresponding neighbor.
        
        :param Point coords: coordinates of the target cell
        :param int walls: wall byte-mask, it removes all walls that are set in the mask
        """
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
        """It alternates the walls at the target cell and its neighbor.
        
        :param Point coords: coordinates of the target cell
        :param int walls: wall byte-mask, it toggles all walls that are set in the mask
        """
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
        """It sets a cell to be dumped."""
        self.dumpCells[coords.x][coords.y] = True
    
    def ignoreCell(self, coords:Tuple[int,int])->None:
        """It sets a cell to not be dumped."""
        self.dumpCells[coords.x][coords.y] = False
    
    def ToggleDumpCell(self, coords:Tuple[int,int])->None:
        """It alternates if the cell will be dumped or not."""
        self.dumpCells[coords.x][coords.y] = not self.dumpCells[coords.x][coords.y]

    def toXML(self):
        """Converts the world to an XML

        :rtype: ElementTree
        """
        ejecucion = ET.Element("ejecucion")
        ejecucion.set("version", self.target_version)
        condiciones = ET.SubElement(ejecucion, "condiciones") # <condiciones instruccionesMaximasAEjecutar="10000000" longitudStack="65000"></condiciones>
        condiciones.set("instruccionesMaximasAEjecutar", f"{self.limits.instruction_limit}")
        condiciones.set("longitudStack", f"{self.limits.stack_size}") 
        condiciones.set("memoriaStack", f"{self.limits.stack_memory}") 
        condiciones.set("llamadaMaxima", f"{self.limits.parameter_limit}") 

        self._buildConditions(condiciones)

        mundos = ET.SubElement(ejecucion, "mundos")

        self._buildWorldXML(mundos)

        programas = ET.SubElement(ejecucion,"programas")
        programas.set("tipoEjecucion", "CONTINUA")
        programas.set("intruccionesCambioContexto", "1") # NOTE: IDK WHAT THIS DOES
        programas.set("milisegundosParaPasoAutomatico", "0") # NOTE: IDK WHAT THIS DOES

        self._buildProgramXML(programas)

        return ET.ElementTree(ejecucion)
    
    def _buildConditions(self, condiciones:ET.Element):
        if self.limits.leave_limit != -1:
            self._buildCondition(condiciones, "DEJA_ZUMBADOR", self.limits.leave_limit)
        if self.limits.pick_limit != -1:
            self._buildCondition(condiciones, "COGE_ZUMBADOR", self.limits.pick_limit)
        if self.limits.move_limit != -1:
            self._buildCondition(condiciones, "AVANZA", self.limits.move_limit)
        if self.limits.left_limit != -1:
            self._buildCondition(condiciones, "GIRA_IZQUIERDA", self.limits.left_limit)

    def _buildCondition(self, condiciones:ET.Element, name:str, value:int):
        comando = ET.SubElement(condiciones, "comando")
        comando.set("nombre", name)
        comando.set("maximoNumeroDeEjecuciones", f"{value}")

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

        for x in range(1, self.width+1):
            for y in range(1, self.height+1):
                if self.dumpCells[x][y]:
                    dump = ET.SubElement(mundo, "posicionDump")
                    dump.set("x", f"{x}")
                    dump.set("y", f"{y}")

    
    def _buildProgramXML(self, programasNode):
        programa = ET.SubElement(programasNode, "programa")

        programa.set("nombre", "p1") # NOTE: idk
        programa.set("ruta","{$2$}") #NOTE: idk
        programa.set("mundoDeEjecucion","mundo_0") 
        programa.set("xKarel",f"{self.karel_x}") 
        programa.set("yKarel",f"{self.karel_y}") 

        
        programa.set(
            "direccionKarel", 
            f"{ORIENTATION_DECODE[self.karel_orientation.value]}"
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

        flag =False
        for rows in self.dumpCells:
            for vals in self.dumpCells:
                flag = flag or vals
        if flag:
            despliega("MUNDO")

    def write(self, path: str, format:bool = True):
        """Writes the XML representation to a file.

        :param str path:  location of the file to write
        :param bool format: if true, it ands indentation, defaults to True
        """
        xml = self.toXML()
        if (format):
            ET.indent(xml, space="\t", level=0)
        xml.write(path)
