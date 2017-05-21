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
   isi_random = 1
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
   def create(self, n, task_interval, rest_interval, isi, ncallback, fs): 
      
      # open figure window
      fig = plt.figure()
      self.text = plt.figtext(0.4,0.5,'Initiating Trial...', fontsize=15)
      plt.ioff()
      #plt.show()
            
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
      
      
      callback_time = ncallback/fs;
      time = np.round(self.start_delay/callback_time)
      cbtimes = zeros(self.events.shape[0])
      for i in range(self.events.shape[0]):
         cbtimes[i] = time
         
         # switch statement
         checkEvent = self.events[i,0]
         if checkEvent == 1:
            time = time + np.round(rest_interval/callback_time)
         elif checkEvent == nc + 2:
            #tisi = 1 + np.random.uniform(0,isi) # the time for the isi interval (random up to isi)
            tisi = isi # the time for the isi interval (fixed at isi seconds)
            time = time + np.round(tisi/callback_time)
         else:
            time = time + np.round(task_interval/callback_time)
            
      self.cb_event = zeros((int(time),2)) # time by 2 matrix of zeros
      
      # sets values at non-zero indices (in cbtimes) to 1 in the 2nd row of cb_event
      self.cb_event[ix_(cbtimes),1] = 1 
      
      # sets values at non-zero indices (in cbtimes) to ev in the 1st row of cb_event
      self.cb_event[ix_(cbtimes),0] = ev.flatten(1)       
      
########################################################################
# PROCESS_EVENT_EMG

def process_event_emg(task,event,runIndex,totalInterval,sessionNumber):

   # switch statement to display the current task
   cueType = task.cue_type[event-1]
   if cueType == 'ISI':
      task.text.set_text('ISI')
      print 'ISI'
      print
   elif cueType == 'start_trial':
      task.text.set_text('Prepare')
      print 'Prepare'
   else:
      task.text.set_text(task.cue[event-1])
      print task.cue[event-1]
      
   
#########################################################################  
# PARADIGM_TEST

sessionNumber = 1

numOfTasks = 2    # number of times each task (left, right, rest) will be displayed 
                  # number of sets of commands = numOfTasks*len(cue)
taskInterval = 2  # number of seconds for the task (left,right,rest)
restInterval = 3  # number of seconds before the task (to prepare)
isiInterval = 5   # inter stimulus interval
totalInterval = taskInterval + restInterval
nCallBack = 1200  # number of samples after which callback is called
fs = 1200         # sampling rate

cue = ['Left','Right','Rest'] # list of cues
cue_type = [] # type of each cue (ex: 'text','audio', etc)
for i in range(len(cue)): # make cue_type the same length as cue
   cue_type.append('text')
#cue_type = ['text', 'text', 'text'] 

sub_cue = ['']
cue_description = ['left flex','rest']
sub_cue_type = ['bar','bar','bar','bar']

# creates the paradigm for a cued hand movement
task = create_paradigm_reach(cue, sub_cue, cue_description, cue_type, sub_cue_type)
task.create(numOfTasks, taskInterval, restInterval, isiInterval, nCallBack, fs)

#print task.cb_event

runIndex = 0 # index of each run of an event

# display 'Initiating Trial'
print 'Initiating Trial'
print

for i in range(1, task.cb_event.shape[0]): # size of task.cb_event's 1st column
   event = int(task.cb_event[i,0]) # set event to number representing the cue (0-4)
   # 0=no change, 1=prepare, 2=left, 3=right 4=rest, 5=ISI      
   
   if event > 0:
      if task.cue_type[event-1] == "start_trial":
         runIndex = runIndex + 1
         
         # create fID file for trial data
         fID = open('emg_session_' + str(sessionNumber) + '.hdr', "a"); # create file (ex: emg_session_1.hdr)
         
         if task.cue[int(task.cb_event[i+2,0])-1] == task.cue[1]: # event type = 'start_trial'
            trialData = task.cue[1] # set trialData to 'Left'
         else:
            trialData = task.cue[2] # set trialData to 'Rest'
         
         # print data to fID file
         fID.write(str(runIndex) + ',' + str(trialData) + ',' + str(datetime.datetime.now()))
         fID.write("\n")
         fID.close()
         
      # processes the current event
      process_event_emg(task,event,runIndex,totalInterval,sessionNumber)
      
   time.sleep(1) # pause for 1 second
            
# display "Ending Trial...'
print 'Ending Trial...'
task.text.set_text('Ending Trial...')
plt.close()
