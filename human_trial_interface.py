from numpy import *
import numpy as np
#import scipy as Sci
#import scipy.linalg
import random
import matplotlib.pyplot as plt
#import pylab
#from pylab import plot,show,close
import time
import datetime


#########################################################
class create_paradigm_reach(object):
   start_delay = 5 # time before the program starts running (when 'Initiating Trial')

   # cue
   # cue_description
   # cue_type
   # events
   # cb_event

   # initializes class
   def __init__(self, cue, sub_cue, cue_description, cue_type, sub_cue_type):
      self.cue = cue  
      self.sub_cue = sub_cue 
      self.cue_description = cue_description  
      self.cue_type = cue_type  
      self.sub_cue_type = sub_cue_type 
   
   # creates cb_event: matrix representing the paradigm with the proper times for each event     
   def create(self, n, task_interval, rest_interval, isi, ncallback, fs, isiRandom): 
      
      # open figure window
      fig = plt.figure(figsize=[3,3]) # opens figure window of 3 x 3 inches
      #plt.ioff() # turns interactive mode on
      self.text = plt.figtext(0.5,0.5,'Initiating Trial...', fontsize=20,
                              horizontalalignment='center',verticalalignment='center')
      plt.pause(5) # pause 5 seconds for Initiating Trial - reimplement in paradigm_test
            
      nc = len(cue) # number of columns in cue
      self.cue = hstack(('+', cue, ' '))
      self.cue_description = hstack(('rest',self.cue_description,'ISI'))
      self.cue_type = hstack(('start_trial',self.cue_type, 'ISI'))
      
      prepareAndISIInclusion = 3
      # sets events to a n*nc*prepareAndISIInclusion by 2 matrix
      self.events = zeros((n*nc*prepareAndISIInclusion, 2)) 

      #repmat in matlab
      cl = tile(r_[2.:nc+2],(n,1)) # n copies of 2 to nc+1
      
      # take rows of cl and put into 1 vector 
      ev = cl.flatten(1) # cl(:) in matlab
      
      # random permutation of numbers in ev vector
      ev = np.random.permutation(ev)

      # concatenate ones(column vector) with ev and column of nc+2
      ones_column = ones((n*nc,1))
      a = c_[ones_column, ev, ones_column*nc + 2]
      
      # transpose
      ev = a.T
      
      # set first column (0-index) in events(zeros vector) to all numbers in ev
      self.events[:,0] = ev.flatten(1)
      
      nsub = len(sub_cue) # length of sub_cue
      if nsub > 1: # for using graded flexing
         cc = ['+']
         cd = ['rest']
         ct = ['start_trial']
         u = 1
         for i in range(len(cue)):
            for j in range(len(sub_cue)):
               cc.append(cue[i] + ':' + sub_cue[j]) # ex: 'left:25'
               cd.append(cue_description[i] + ':' + sub_cue[j]) # ex: 'left_flex:25'
               ct.append(cue_type[i] + ':' + sub_cue_type[j]); # ex: 'text:bar'
         
         cc.append(' ')
         cd.append('ISI')
         ct.append('ISI')
         self.cue = cc
         self.cue_description = cd
         self.cue_type = ct
         
         ev = self.events[:,0] # all data in the first column of self.events
         evn = np.zeros((n*nc*prepareAndISIInclusion + n*nc*(nsub-1)))
         evn[0:evn.shape[0]:(nsub+2)] = 1 # set every nsub+2 value equal to 1 starting from 0 until the end
         evn[(nsub+1):evn.shape[0]:(nsub+2)] = nc*nsub+2 # set every nsub+2 value to nc*nsub+2 starting from nsub+1 until the end
         
         for k in range(1, nsub+1):
            endPoint = evn.shape[0]
            rangeTemp = np.arange(0,endPoint,nsub+2)
            indices = np.array(rangeTemp)
            logicalTemp = logical_and((ev > 1) , (ev < (nc+2))) # boolean array with True's at indicies where both statements are true
            evn[indices+k] = (ev[logicalTemp]-2)*nsub+k+1 # take data from ev at non-zero valued indices in logicalTemp
         
         nc = nsub*nc
         self.events = zeros((evn.shape[0],2))
         self.events[:,0] = evn
         ev = evn
      
      callback_time = ncallback/fs;
      time = np.round(self.start_delay/callback_time)
      cbtimes = zeros((self.events.shape[0])).astype(int)
      for i in range(self.events.shape[0]):
         cbtimes[i] = time
         
         # switch statement
         checkEvent = self.events[i,0]
         if checkEvent == 1:
            time = time + np.round(rest_interval/callback_time)
         elif checkEvent == nc + 2:
            if isiRandom == True:
               tisi = 1 + np.random.uniform(0,isi) # the time for the isi interval (random up to isi)
            else:
               tisi = isi # the time for the isi interval (fixed at isi seconds)
            
            time = time + np.round(tisi/callback_time)
         else:
            time = time + np.round(task_interval/callback_time)
            
      self.cb_event = zeros((int(time),2)) # time by 2 matrix of zeros

      # sets values at non-zero indices (in cbtimes) to 1 in the 2nd column of cb_event
      self.cb_event[cbtimes,1] = 1 
      
      # sets values at non-zero indices (in cbtimes) to ev in the 1st column of cb_event
      self.cb_event[cbtimes,0] = ev.flatten(1)       
      
########################################################################
# PROCESS_EVENT_EMG

def process_event_emg(task,event,runIndex,totalInterval,sessionNumber):
   
   # switch statement to display the current task
   cueType = task.cue_type[event-1]
   if cueType == 'ISI':
      task.text.set_text('ISI')
      print 'ISI'
      print
      plt.pause(.01)                      
   elif cueType == 'start_trial':    
      task.text.set_text('Prepare')
      print 'Prepare'
      plt.pause(.01)                      
   else:   
      task.text.set_text(task.cue[event-1])
      print task.cue[event-1]
      plt.pause(.01)                
      
#########################################################################  
# PARADIGM_TEST

sessionNumber = 1

numOfTasks = 2    # number of times each task (left, right, rest) will be displayed 
                  # number of sets of commands = numOfTasks*len(cue)
taskInterval = 2  # number of seconds for the task (left,right,rest)
restInterval = 2  # number of seconds before the task (to prepare)
isiInterval = 4   # inter stimulus interval
isiRandom = False # whether isiInterval is random or not
totalInterval = taskInterval + restInterval
nCallBack = 1200  # number of samples after which callback is called
fs = 1200         # sampling rate
useGradedFlexing = True

cue = ['Left','Right','Rest'] # list of cues
cue_type = [] # type of each cue (ex: 'text','audio', etc)
for i in range(len(cue)): # make cue_type the same length as cue
   cue_type.append('text')
#cue_type = ['text', 'text', 'text'] 

if useGradedFlexing:
   sub_cue = ['25','50','75','100'] # for graded flexing
else:
   sub_cue = ['']
   
cue_description = ['left flex','right flex','rest']
sub_cue_type = ['bar','bar','bar','bar']

# creates the paradigm for a cued hand movement
task = create_paradigm_reach(cue, sub_cue, cue_description, cue_type, sub_cue_type)
task.create(numOfTasks, taskInterval, restInterval, isiInterval, nCallBack, fs, isiRandom)

#print task.cb_event        
#print task.cue

runIndex = 0 # index of each run of an event to be recorded to a file

# display 'Initiating Trial'
print 'Initiating Trial...'
print

for i in range(1, task.cb_event.shape[0]): # size of task.cb_event's 1st column
   event = int(task.cb_event[i-1,0]) # set event to number representing the cue (0-5) (non-graded flexing)
   # 0=no change, 1=prepare, 2=left, 3=right 4=rest, 5=ISI (non-graded flexing)
   
   if event > 0:
      # (at prepare) or (using graded flexing and not recording ISI and ISI interval)
      if task.cue_type[event-1] == "start_trial" or (useGradedFlexing and int(task.cb_event[i-1 + restInterval,0]) != 14 and event != 14):
         runIndex = runIndex + 1
         
         # create fID file for trial data
         fID = open('emg_session_' + str(sessionNumber) + '.hdr', "a"); # create file (ex: emg_session_1.hdr)
         
         # task.cue: ['+',"Left','Right','Rest',' '] (non-graded flexing)

         # cue at restInterval indices after the current index
         trialData = task.cue[int(task.cb_event[i-1 + restInterval,0])-1]  
         
         # print data to fID file (restInterval seconds before the actual cue is displayed)
         fID.write(str(runIndex) + ',' + str(trialData) + ',' + str(datetime.datetime.now()))
         fID.write("\n") # write the next data on the next line
         fID.close()
         
      # processes the current event
      process_event_emg(task,event,runIndex,totalInterval,sessionNumber)
   
   if i > 5 and event > 0: # 'Initiating Trial' has already been paused for 5 seconds and pause(0.01) was already called in process_event_emg
      time.sleep(0.99)
   elif event == 0: # process_event_emg is not executed, so the full 1 second pause is needed here
      time.sleep(1)
            
# display "Ending Trial...'
print 'Ending Trial...'
task.text.set_text('Ending Trial...')
plt.pause(3) 
#plt.close() # closes figure window
