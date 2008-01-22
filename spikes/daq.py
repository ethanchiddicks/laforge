#Acq_IncClk.py

# This is a near-verbatim translation of the example program
# C:\Program Files\National Instruments\NI-DAQ\Examples\DAQmx ANSI C\Analog In\Measure Voltage\Acq-Int Clk\Acq-IntClk.c

import ctypes
import numpy

nidaq = ctypes.windll.nicaiu # load the DLL

##############################
# Setup some typedefs and constants
# to correspond with values in
# C:\Program Files\National Instruments\NI-DAQ\DAQmx ANSI C Dev\include\NIDAQmx.h

# the typedefs
int32 = ctypes.c_long
uInt32 = ctypes.c_ulong
uInt64 = ctypes.c_ulonglong
float64 = ctypes.c_double
TaskHandle = uInt32

# the constants
DAQmx_Val_Cfg_Default = int32(-1)
DAQmx_Val_RSE = int32(10083)
DAQmx_Val_Diff = int32(10106)
DAQmx_Val_Volts = 10348
DAQmx_Val_Rising = 10280
DAQmx_Val_FiniteSamps = 10178
DAQmx_Val_ContSamps = 10123
DAQmx_Val_HWTimedSinglePoint = 12522
DAQmx_Val_GroupByChannel = 0
##############################

def CHK(err):
    """a simple error checking routine"""
    if err < 0:
        buf_size = 100
        buf = ctypes.create_string_buffer('\000' * buf_size)
        nidaq.DAQmxGetErrorString(err,ctypes.byref(buf),buf_size)
        raise RuntimeError('nidaq call failed with error %d: %s'%(err,repr(buf.value)))

# initialize variables
taskHandle = TaskHandle(0)
max_num_samples = 2
data = numpy.zeros((max_num_samples,),dtype=numpy.float64)

# Channel 0
CHK(nidaq.DAQmxCreateTask("",
	ctypes.byref(taskHandle))
	)

CHK(nidaq.DAQmxCreateAIVoltageChan(taskHandle,
				"Dev1/ai8, Dev1/ai0",
				"",   
				DAQmx_Val_Cfg_Default,
                                float64(-10.0),float64(10.0),
                                DAQmx_Val_Volts,None))

#CHK(nidaq.DAQmxCfgSampClkTiming(taskHandle, # taskHandle
#				"", # source
#				float64(40.0), # rate
#                                DAQmx_Val_Rising, # activeEdge
#				DAQmx_Val_FiniteSamps, # sampleMode
#                                uInt64(2) # sampsPerChanToAcquire
#				)
#				)
CHK(nidaq.DAQmxStartTask(taskHandle))

def read_daq():
	read = int32()
	CHK(nidaq.DAQmxReadAnalogF64(taskHandle, # taskHandle
				1, # numSampsPerChan
				float64(10.0), # timeout
                             	DAQmx_Val_GroupByChannel, # fillMode
				data.ctypes.data, # readArray
				2, # arraySizeInSamps
				ctypes.byref(read), # sampsPerChanRead
				None) # reserved
				)
	#print "Acquired %d points"%(read.value)
	#print data
	return data

#if taskHandle.value != 0:
#    nidaq.DAQmxStopTask(taskHandle)
#    nidaq.DAQmxClearTask(taskHandle)

#print "End of program, press Enter key to quit"
#raw_input()
