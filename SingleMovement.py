# Run it as Administrator, otherwise the usb port cannot be reached.
from ctypes import *
from time import sleep

class _USB1020_PARA_DO(Structure):
    _fields_ = [("OUT0", c_uint),
                ("OUT1", c_uint),
                ("OUT2", c_uint),
                ("OUT3", c_uint),
                ("OUT4", c_uint),
                ("OUT5", c_uint),
                ("OUT6", c_uint),
                ("OUT7", c_uint)]
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
AxisNum=0
MoveDir=1
PulNum=(5e5/100)*2 ## about 2 mm

dllpath='D:\\profiler\\i386\\USB1020_32.dll'
test = windll.LoadLibrary(dllpath)

DevHdl=test.USB1020_CreateDevice(0)
ResultSetLP=test.USB1020_SetLP(DevHdl,1,0)
PAPA=pointer(_USB1020_PARA_DO(1,1,1,1,1,1,1))
test.USB1020_SetDeviceDO(DevHdl, AxisNum, PAPA)


pDL=pointer(_USB1020_PAPA_DataList(MultiRatio,1000,4000,500,125,6000,6000))
pLC=pointer(_USB1020_PAPA_LCData(AxisNum,0,0,1,0,0,0,MoveDir,int(PulNum)))
test.USB1020_InitLVDV(DevHdl,pDL,pLC)
test.USB1020_StartLVDV(DevHdl,AxisNum)
while test.USB1020_ReadCV(DevHdl,AxisNum):
    print test.USB1020_ReadCV(DevHdl,AxisNum)

ResultReleaseDevice=test.USB1020_ReleaseDevice(DevHdl)


