from numpy import array
from math import ceil
import matplotlib.pyplot as plt
import visa
from ctypes import *
from time import sleep

def CreateGPIB(fmin,fmax,NF):
    IFBW='3KHZ';
##    fmin,fmax,NF=9,20,3201
    
    rm = visa.ResourceManager()
##    rm.list_resources()
    inst = rm.open_resource('GPIB0::16::INSTR')
    print(inst.query("*IDN?"))

    surfix="; *OPC?"
    inst.query("SYST:FPR"+surfix)
    inst.query("DISP:WIND ON"+surfix)
    inst.query('CALC:PAR:DEF "MyMeas",S21'+surfix)
    inst.query('DISP:WIND:TRAC:FEED "MyMeas"'+surfix)

    inst.query('SENS:FREQ:STAR '+str(fmin)+'ghz'+surfix)
    inst.query('SENS:FREQ:STOP '+str(fmax)+'ghz'+surfix)
    inst.query('SENS:SWE:POIN '+str(NF)+surfix)
    inst.query('SENS:BWID '+IFBW+surfix)
    return inst
    
def DoMeasurement(GPIBH):
    surfix="; *OPC?"
    inst.query('INIT:CONT OFF'+surfix)
    inst.query('INIT:IMM;*wai'+surfix)
    data = inst.query('CALC:DATA? SDATA'+surfix)
    return data

def CreateUSB(test):
    class _USB1020_PARA_DO(Structure):
        _fields_ = [("OUT0", c_uint),
                    ("OUT1", c_uint),
                    ("OUT2", c_uint),
                    ("OUT3", c_uint),
                    ("OUT4", c_uint),
                    ("OUT5", c_uint),
                    ("OUT6", c_uint),
                    ("OUT7", c_uint)]
##    dllpath='f:\\Desktop\\profiler\\i386\\USB1020_32.dll'
##    test = windll.LoadLibrary(dllpath)
    DevHdl=test.USB1020_CreateDevice(0)
    ResultSetLP=test.USB1020_SetLP(DevHdl,1,0)
    PAPA=pointer(_USB1020_PARA_DO(1,1,1,1,1,1,1))
    test.USB1020_SetDeviceDO(DevHdl, 0, PAPA)
    test.USB1020_SetDeviceDO(DevHdl, 1, PAPA)
    return DevHdl

def MoveXY(test,DevHdl,AxisNum,PulNum):
    class _USB1020_PAPA_DataList(Structure):
        _fields_ = [("Multiple", c_long),
                    ("StartSpeed", c_long),
                    ("DriveSpeed", c_long),
                    ("Acceleration", c_long),
                    ("Deceleration", c_long),
                    ("AccIncRate", c_long),
                    ("DecIncRate", c_long)]
    class _USB1020_PAPA_LCData(Structure):
        _fields_ = [("AxisNum", c_long),
                    ("LV_DV", c_long),
                    ("DecMode", c_long),
                    ("PulseMode", c_long),
                    ("PLSLogLever", c_long),
                    ("DIRLogLever", c_long),
                    ("Line_Curve", c_long),
                    ("Direction", c_long),
                    ("nPulseNum", c_long)]
    MultiRatio=40
    MoveDir=1 if (PulNum>0 and AxisNum==0) or (PulNum<0 and AxisNum==1) else 0
    PulNum=abs(PulNum)
    pDL=pointer(_USB1020_PAPA_DataList(MultiRatio,1000,4000,500,125,6000,6000))
    pLC=pointer(_USB1020_PAPA_LCData(AxisNum,0,0,1,0,0,0,MoveDir,int(PulNum)))
    test.USB1020_InitLVDV(DevHdl,pDL,pLC)
    test.USB1020_StartLVDV(DevHdl,AxisNum)
##    sleep(1)#################################
    while test.USB1020_ReadCV(DevHdl,AxisNum):
##        print test.USB1020_ReadCV(DevHdl,AxisNum)
        pass

def Serpentine(Mat,NX,NY,flag):
    temp=Mat
    if flag:
        temp=[[Mat[(xi if 1-(yi % 2) else NX-xi-1)][yi] for xi in range(NX)] for yi in range(NY)]
    temp=array(temp)
    temp=temp.flatten()
    SnakeMat=list(temp)
    return SnakeMat

##########################################
###################### MAIN PART #########
##########################################

##########################################
###################### parameters ########
##########################################
x,dx = 350, 3.5
y,dy = x, dx
SF,EF,NP = 9, 20, 801
Xpdr,Ypdr=5e5/100, 5e5/100
##########################################
dllpath='D:\\profiler\\i386\\USB1020_32.dll'
test = windll.LoadLibrary(dllpath)
###################### this block can be realized by Matplotlib as well
NX=int(ceil((x+1/1e5)/dx))
NY=int(ceil((y+1/1e5)/dy))

NMX=[[xi for xi in range(NX)] for yi in range(NY)]
NMY=[[yi for xi in range(NX)] for yi in range(NY)]

PMX=[[round(xi*Xpdr*dx) for xi in range(NX)] for yi in range(NY)]
PMY=[[round(yi*Ypdr*dy) for xi in range(NX)] for yi in range(NY)]

SnNMX=Serpentine(NMX,NX,NY,1)
SnNMY=Serpentine(NMY,NX,NY,1)
SnPMX=Serpentine(PMX,NX,NY,1)
SnPMY=Serpentine(PMY,NX,NY,1)

##########################################
###################### create GPIB and USB
##########################################
inst=CreateGPIB(SF,EF,NP)
DevHdl=CreateUSB(test)

##########################################
###################### Move and Measure ##
##########################################
for ii in range(len(SnPMX)):
    print ii
    
    II=(ii)%(NX*NY)
    II_1=(ii+1)%(NX*NY)
    
    filename='./X'+str(int(SnNMX[II]))+'Y'+str(int(SnNMY[II]))+'.txt'    
    S=DoMeasurement(inst) ## Measure and Save data
    f = open(filename,'w')
    f.write(S)
    f.close()
    
    MoveXY(test,DevHdl,0,int(SnPMY[II_1]-SnPMY[II])) ## MoveXY(DevH,AxisNum,PulNum);
    MoveXY(test,DevHdl,1,int(SnPMX[II_1]-SnPMX[II])) ## x=1, y=0, x+=1, x-=0, y+=0, y-=1

##########################################
#################### clean up GPIB and USB
##########################################
ResultReleaseDevice=test.USB1020_ReleaseDevice(DevHdl)
