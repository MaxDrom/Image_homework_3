from math import copysign, pow
from urllib.request import urlopen
import matplotlib.pyplot as plt
import numpy as np

def get_galaxies(type : str):
    max_count = 1000
    result = []
    count = 0
    with open(f"{type}.cgi") as file:
        for line in file.readlines():
            if(count>max_count):
                break
            if line.startswith("!"):
                continue
            params  = line.split("|")
            RA = params[0].split(' ')[1:4]
            RAdeg = 15*float(RA[0])+15.0*float(RA[1])/60.0+15*float(RA[2])/3600.0
            DEC = params[0].split(' ')[4:7]
            DECdeg = copysign(abs(float(DEC[0]))+float(DEC[1])/60.0+float(DEC[2])/3600.0, float(DEC[0]))
            try:
                log25d = float(params[2])
            except:
                continue
            d = 10*pow(10, log25d)
            scale = min(max(0.015, d/150), 60)
            url = f"https://skyserver.sdss.org/dr14/SkyServerWS/ImgCutout/getjpeg?TaskName=Skyserver.Explore.Image&ra={RAdeg}&dec={DECdeg}&scale={scale}&width=200&height=200"
            with urlopen(url) as req:
                result.append(plt.imread(req, format="jpeg"))
                count+=1
    return np.array(result)


spirals = get_galaxies("spirals")
edges = get_galaxies("edge")
elliptic = get_galaxies("elliptic")