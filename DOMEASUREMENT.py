import visa
rm = visa.ResourceManager()
rm.list_resources()

IFBW='3KHZ';
fmin=9
fmax=20
NF=3201

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

inst.query('INIT:CONT OFF'+surfix)
inst.query('INIT:IMM;*wai'+surfix)
a = inst.query('CALC:DATA? SDATA'+surfix)
xi=1
yi=1
f = open('./X'+str(xi)+'Y'+str(yi)+'.txt','w')
f.write(a)
f.close()
