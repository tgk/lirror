#!/usr/bin/env python
import inkex
from lxml import etree
from inkex.transforms import Transform
import copy
import math

class Lirror(inkex.EffectExtension):
    def __init__(self):
            inkex.Effect.__init__(self)

    def add_arguments(self, pars):
        pars.add_argument("--copies", type=int, default="10")

        pars.add_argument("--angle", type=float, default="45")
        pars.add_argument("--angleincrement", default="linear")
        pars.add_argument("--sinusidalscale", type=float, default="1")

        pars.add_argument("--deltax", type=float, default="0")
        pars.add_argument("--deltay", type=float, default="0")
        pars.add_argument("--deltaincrement", default="linear")
        pars.add_argument("--deltasinusidalscale", type=float, default="1")

        pars.add_argument("--scalex", type=float, default="0")
        pars.add_argument("--scaley", type=float, default="0")

    def effect(self):
        obj = self.svg.selected[self.options.ids[0]]
        group = etree.SubElement(obj.getparent(),inkex.addNS('g','svg'))
        mat = Transform([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
        theta = math.radians(self.options.angle)
        for n in range(self.options.copies):
            cpy = copy.deepcopy(obj)
            group.append(cpy)

            scaledTheta = theta
            if self.options.angleincrement == "sinusidal":
              scaledTheta = theta * (1 + math.sin(n * self.options.sinusidalscale))/2.0
            rotationMat = Transform([[math.cos(scaledTheta), math.sin(scaledTheta), 0], [-math.sin(scaledTheta), math.cos(scaledTheta), 0]])

            deltaScale = 1
            if self.options.deltaincrement == "sinusidal":
              deltaScale = (1 + math.sin(n * self.options.deltasinusidalscale))/2.0
            translationMat = Transform([[1, 0, self.options.deltax*deltaScale], [0, 1, self.options.deltay*deltaScale]])

            scaleMat = Transform([[self.options.scalex, 0, 0], [0, self.options.scaley, 0]])

            mat = mat * rotationMat * translationMat * scaleMat

            cpy.transform=mat

if __name__ == '__main__':
    Lirror().run()
