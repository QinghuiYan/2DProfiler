from ctypes import *
dllpath='D:\\profiler\\i386\\USB1020_32.dll'  
#test2 = CDLL(dllpath)
test  = windll.LoadLibrary(dllpath)

AxisNum=0
DevHdl=test.USB1020_CreateDevice(0)
ResultSetLP=test.USB1020_SetLP(DevHdl,1,0)
ResultSetLP=test.USB1020_SetEP(DevHdl,1,0)
###################
class _USB1020_PARA_DO(Structure):
    _fields_ = [("OUT0", c_uint),
                ("OUT1", c_uint),
                ("OUT2", c_uint),
                ("OUT3", c_uint),
                ("OUT4", c_uint),
                ("OUT5", c_uint),
                ("OUT6", c_uint),
                ("OUT7", c_uint)]
PAPA=pointer(_USB1020_PARA_DO(1,1,1,1,1,1,1))
test.USB1020_SetDeviceDO(DevHdl, AxisNum, PAPA)

###############
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
pDL=pointer(_USB1020_PAPA_DataList(10,1000,4000,140,125,1000,1000))
pLC=pointer(_USB1020_PAPA_LCData(AxisNum,0,0,1,0,0,0,1,50000))

test.USB1020_InitLVDV(DevHdl,pDL,pLC)
#################

test.USB1020_StartLVDV(DevHdl,AxisNum)
#test.USB1020_DecStop
ResultReleaseDevice=test.USB1020_ReleaseDevice(DevHdl)
