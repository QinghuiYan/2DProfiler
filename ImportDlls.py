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

#test.USB1020_InitLVDV.argtypes=[c_long, c_int, c_int]####
##test.USB1020_InitLVDV.argtypes=[c_long,c_int,c_int,c_int]
##aa=(test.PUSB1020_PARA_DataList)(a)
##bb=(test.PUSB1020_PAPA_LCData)(b)
test.USB1020_InitLVDV(DevHdl,pDL,pLC)
#################

test.USB1020_StartLVDV(DevHdl,AxisNum)
#test.USB1020_DecStop
ResultReleaseDevice=test.USB1020_ReleaseDevice(DevHdl)
print 'mmb'



##typedef struct _USB1020_PAPA_DataList
##{
##	LONG Multiple;	    	// Multi ratio (1~500)
##	LONG StartSpeed;	// StartSpeed(1~8000)
##	LONG DriveSpeed;	// DriveSpeed(1~8000)
##	LONG Acceleration;	// Acc(125~1000000)
##	LONG Deceleration;	// Dec(125~1000000)
##	LONG AccIncRate;	// Acc Rate(954~62500000)
##	LONG DecIncRate;	// Dec Rate(954~62500000)
##} USB1020_PARA_DataList, *PUSB1020_PARA_DataList;

##typedef struct _USB1020_PAPA_LCData
##{
##	LONG AxisNum;		// Axis num (X | Y | X\Y axis)
##	LONG LV_DV;		// Drive mode  (Continuous | Fixed )
##	LONG DecMode;		// Dec mode(Auto | Manual)	
##	LONG PulseMode;		// Pulse mode (CW/CCW | CP/DIR)
##	LONG PLSLogLever;	// Set pulse dir
##	LONG DIRLogLever;	// Direction signal level(0:L-level +dir H-level -dir, 1:H-level +dir L-level -dir)		
##	LONG Line_Curve;	// Movement mode(Linear | S-shaped)
##	LONG Direction;		// Movement direction 
##	LONG nPulseNum;		// Pulse Num(0~268435455)
##} USB1020_PARA_LCData, *PUSB1020_PARA_LCData;
