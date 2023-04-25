from math import copysign, pow, ceil, log
from urllib.request import urlopen
import matplotlib.pyplot as plt
import numpy as np
import sys

max_count = int(sys.argv[1])
def get_galaxies(type : str):
    result = []
    count = 0
    with open(f"{type}.cgi") as file:
        for line in file.readlines():
            if(count>=max_count):
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
            d = pow(10, log25d)/10
            if(d*60<15):
                continue
            scale = min(max(0.015, 1.05*d*60/64), 60)
            url = f"https://skyserver.sdss.org/dr14/SkyServerWS/ImgCutout/getjpeg?TaskName=Skyserver.Explore.Image&ra={RAdeg}&dec={DECdeg}&scale={scale}&width=64&height=64"
            #url = f"https://skyserver.sdss.org/dr14/SkyServerWS/ImgCutout/getjpeg?TaskName=Skyserver.Explore.Image&ra={RAdeg}&dec={DECdeg}&scale=0.015&width={ceil(d*100)}&height={ceil(d*100)}"
            with urlopen(url) as req:
                with open(f"pictures/{type}_{count}.jpg", "wb") as result:
                    result.write(req.read())
                count+=1
    return np.array(result)

edges = get_galaxies("edge")
elliptic = get_galaxies("elliptic")
spirals = get_galaxies("spirals")