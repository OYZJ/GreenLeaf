# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 21:17:31 2018

@author: Dong
"""

from skimage.measure import label, regionprops
import matplotlib.image as mpimg


def feature_extraction(path):
    Img=mpimg.imread(path)
    Img=Img/255
    label_img1 = label(Img,neighbors=8,background=0)
    region1 = regionprops(label_img1)

    LeafProp={}
    LeafProp["Area"]=region1[0].area
    LeafProp["Perimeter"] =region1[0].perimeter
    LeafProp["MinL"]=region1[0].minor_axis_length
    LeafProp["MaxL"]=region1[0].major_axis_length
    LeafProp["Eccentricity"]=region1[0].eccentricity
    LeafProp["Solidity"]=region1[0].solidity
    LeafProp["Orientation"]=region1[0].orientation
    LeafProp["Equivalent_diameter"]=region1[0].equivalent_diameter
    LeafProp["Convex_area"]=region1[0].convex_area
    LeafProp["Bbox_area"]=region1[0].bbox_area
    return LeafProp

