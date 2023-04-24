from math import copysign

table2 = open("GalaxyZoo1_DR_table2.csv").readlines()
sp_sample = open("sp.dat", "w")
el_sample = open("el.dat", "w")
ed_sample = open("ed.dat", "w")
for obj in table2[1:]:
    params = obj.split(',')
    OBJID = int(params[0])
    RA = params[1].split(':')
    RAdeg = 15*float(RA[0])+15.0*float(RA[1])/60.0+15*float(RA[2])/3600.0
    DEC = params[2].split(':')
    DECdeg = copysign(abs(float(DEC[0]))+float(DEC[1])/60.0+float(DEC[2])/3600.0, float(DEC[0]))
    NVOTE = int(params[3])
    P_EL = float(params[4])
    P_CW = float(params[5])
    P_ACW = float(params[6])
    P_EDGE = float(params[7])
    if((P_CW>0.8) or (P_ACW>0.8)):
        sp_sample.write(f'nearest:B {" ".join(RA)} {" ".join(DEC)}\n')
    if(P_EDGE>0.8):
        ed_sample.write(f'nearest:B {" ".join(RA)} {" ".join(DEC)}\n')
    if(P_EL>0.8):
        el_sample.write(f'nearest:B {" ".join(RA)} {" ".join(DEC)}\n')