from typing import Dict, List
from KarelInput import KarelInputCase
from KarelUtil import *
import io


import xml.etree.ElementTree as ET

# <resultados>
# 	<mundos>
# 		<mundo nombre="mundo_0">


# FIXME: typing
class KarelOutputCase:

    def __init__(
        self, 
        *, 
        beeperBag=None,
        end_x=None,
        end_y=None,
        orientation:Orientation=None
    ):
        self.orientation:Orientation = Orientation.NORTH
        self.karel_x:int = end_x
        self.karel_y:int = end_y
        self.karel_orientation: Orientation = orientation
        self.karel_beepers: int = beeperBag

        self.beepers:Dict[Point, int]={}

    def setBeepers(self, coords:Point, ammount:int):
        self.beepers[coords] = ammount

    def setOrientation(self, orientation:Orientation):
        self.karel_orientation = orientation

    def setPosition(self, coords:Point):
        self.karel_x = coords.x
        self.karel_y = coords.y

    def copyFromInput(
        self, 
        input:KarelInputCase, 
        *, 
        position:bool=True,
        orientation:bool=True,
        beeperBag:bool=True,
        worldBeepers:bool=False,
    ):
        if orientation:
            self.karel_orientation = input.karel_orientation
        if position:
            self.karel_x = input.karel_x
            self.karel_y = input.karel_y
        if beeperBag:
            self.karel_beepers = input.karel_beepers
        if worldBeepers:
            self.beepers = input.beepers.copy()

    def cleanValues(self, input:KarelInputCase):
        self.cleanKarelValues(input.evaluationFlags)
        self.cleanBeepers(input.evaluationFlags, input.dumpCells)

    def cleanKarelValues(self, evaluationFlags: EvalFlags):
        if (evaluationFlags & EvalFlags.BEEPERBAG)==0:
            self.karel_beepers = None
        if (evaluationFlags & EvalFlags.ORIENTATION)==0:
            self.karel_orientation = None
        if (evaluationFlags & EvalFlags.POSITION)==0:
            self.karel_x = None
            self.karel_y = None

    def cleanBeepers(self,  evaluationFlags: EvalFlags, dumpCells: List[List[bool]]) ->None:
        if (evaluationFlags & EvalFlags.ALLBEEPERS)!=0:
            return
        self.beepers = {
            coord : value
            for coord, value in self.beepers.items()
            if (dumpCells[coord.x][coord.y])
        }

        


    def toXML(self, input:KarelInputCase = None):
        if (input != None):
            self.cleanValues(input)
        

        resultados = ET.Element("resultados")

        mundos = ET.SubElement(resultados, "mundos")

        mundo = ET.SubElement(mundos, "mundo")
        mundo.set("nombre", "mundo_0")

        self._buildBeepersXML(mundo)

        programas = ET.SubElement(resultados,"programas")

        programa = ET.SubElement(programas, "programa")
        # nombre="p1" resultadoEjecucion="FIN PROGRAMA"
        programa.set("nombre", "p1")
        programa.set("resultadoEjecucion", "FIN PROGRAMA")
        if (
            self.karel_x != None
            or self.karel_beepers != None 
            or self.karel_beepers != None
            or self.karel_orientation != None
        ):
            karel = ET.SubElement(programa, "karel")
            if (self.karel_x!=None):
                karel.set("x", f"{self.karel_x}")
                karel.set("y", f"{self.karel_y}")

            if (self.karel_orientation!=None):
                karel.set("direccion", f"{ORIENTATION_DECODE[self.karel_orientation.value[0]]}")

            if (self.karel_beepers!=None):
                karel.set("x", f"{self.karel_x}")
                karel.set(
                    "mochila", 
                    f"{self.karel_beepers}") if self.karel_beepers != -1 else "INFINITO"


        return ET.ElementTree(resultados)

    def _buildBeepersXML(self, mundo):
        prevRow = -1
        prevCol = -1
        currentRow=[]
        currentGroup=[]
        startX = -1

        def drawBeeperline():
            linea = ET.SubElement(mundo, "linea")
            linea.set("fila", f"{prevRow}")
            linea.set("compresionDeCeros", f"true")
            text = [
                f"({group[0]}) "
                + "".join([f"{val} " for val in group[1]])
                for group in currentRow
            ]
            text = "".join(text)
            linea.text = text
            
                    
        for coords in sorted(self.beepers.keys(), key=lambda k:(-k.y, k.x)):
            value = self.beepers[coords]
            if prevRow != coords.y:
                if len(currentGroup)!=0:
                    currentRow.append((startX, currentGroup))
                if len(currentRow)!=0:
                    drawBeeperline()
                currentRow=[]                
                currentGroup=[]
            
            if prevCol+1 != coords.x:
                if len(currentGroup)!=0:
                    currentRow.append((startX, currentGroup))
                currentGroup = []
                startX = coords.x

            prevRow = coords.y
            prevCol = coords.x
            currentGroup.append(value)

        
        if len(currentGroup)!=0:
            currentRow.append((startX, currentGroup))

        if len(currentRow)!=0:
            drawBeeperline()



    def write(self, path:str, *, format:bool=False, input:KarelInputCase = None):
        xml = self.toXML(input)
        if (format):
            ET.indent(xml, space="\t", level=0)
        txt=None
        with io.StringIO() as output:
            xml.write(output, encoding="unicode")
            txt = output.getvalue().replace(" />", "/>")
        with open(path, mode="w") as f:
            f.write(txt)



