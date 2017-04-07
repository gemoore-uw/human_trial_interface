
import numpy as np
import scipy
import matcompat
import matplotlib

# from process_event_emg import process_event_emg
# from create_paradigm_reach import create_paradigm_reach

# if available import pylab (from matlibplot)
try:
    import matplotlib.pylab as plt
except ImportError:
    pass

sessionNumber = 1.
numOfTasks = 5.
#%this is numOfTasks of each cue
taskInterval = 2.
restInterval = 2.
isiInterval = 4.
nCallBack = 1200.
fs = 1200.
cue = np.hstack(('Left', 'Rest'))
sub_cue = np.hstack(('25', '50', '75', '100'))
#%{''};%
cue_description = np.hstack(('left flex', 'rest'))
cue_type = np.hstack(('text', 'text'))
sub_cue_type = np.hstack(('bar', 'bar', 'bar', 'bar'))

cb_event = 0

fig, ax = plt.subplots(1) #[int('Position')-1,int(np.array(np.hstack((8.2, 46.6, 753., 832.))))-1]
fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')

textStr = 'HERE'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.00, 0.6, textStr, transform=ax.transAxes, fontsize=50, verticalalignment='top', bbox=props)
#paradigm.text = text[int(0.00)-1,int(0.6)-1,int('+')-1,int('FontSize')-1,59,int('HorizontalAlignment')-1,int('center')-1]
#% fixation cross
#paradigm.bar = rectangle('Position', np.array(np.hstack((0., -.1, .1, .2))), 'FaceColor', 'b', 'Visible', 'off')
ax.add_patch(
    patches.Rectangle(
    (0., -0.1),   # (x,y)
    0.1,          # width
    0.2,          # height
    facecolor = "none",
    edgecolor = "none",
    )
)
plt.xlim(np.array(np.hstack((-1., 1.))))
plt.ylim(np.array(np.hstack((-1., 1.))))
plt.axis('off')
plt.show()


def create_paradigm_reach(n, task_interval, rest_interval, isi, ncallback, fs, cue, sub_cue, cue_description, cue_type, sub_cue_type):

    # Local Variables: figure, cl, cc, text, cbtimes, start_delay, rest_interval, marker, ev, ct, photodiode, nc, cue_type, callback_time, cue, task_interval, cue_description, nsub, events, sub_cue_type, tisi, fs, cd, a, bar, evn, i, sub_cue, j, n, isi, isi_random, u, ncallback, time, cb_event, paradigm
    # Function calls: randi, round, xlim, reshape, randperm, create_paradigm_reach, strcat, ones, zeros, repmat, ylim, rectangle, size
    #% this creates the paradigm for a cued hand movement
    #% n = number of tasks
    #% task_interval = number of seconds for the task
    #% rest_interval = number of seconds before the task for restperiod
    #% isi = inter stimulus interval 
    #% ncallback= number of samples after which callback is called
    #% fs = sampling rate
    #% cue= list of cues
    #% cue_description = description
    #% cue_type = 'text','audio' etc
    # paradigm.figure = figure[int('Position')-1,int(np.array(np.hstack((8.2, 46.6, 753., 832.))))-1]

    start_delay = 5.
    #% wait for 10 sbefore actually doing somehting
    #paradigm.isi_random = 1.
    isi_random = 1.
    #% we want random ISI
    nc = np.size(cue)
    #paradigm.cue = np.array(np.hstack(('+', cue, ' ')))
    cue = np.array(np.hstack(('+', cue, ' ')))
    #%paradigm.cue={'+','left','right',''}; % we have three cues
    #paradigm.cue_description = np.array(np.hstack(('rest', cue_description, 'ISI')))
    cue_description = np.array(np.hstack(('rest', cue_description, 'ISI')))

    #% what happens at each cue
    #paradigm.cue_type = np.array(np.hstack(('start_trial', cue_type, 'ISI')))
    cue_type = np.array(np.hstack(('start_trial', cue_type, 'ISI')))
    #paradigm.events = np.zeros((np.dot(n, nc)*3.), 2.)

    events = np.zeros((int(n*nc*3), int(2)))

    #paradigm = np.zeros(1, 'names':['start_delay', 'isi_random', 'cue', 'cue_description', 'cue_type'],'formats':['i4','i4','a10'])
    paradigm = np.zeros(1, dtype =[('start_delay','i4'),('isi_random','i4'),('cue','a10',np.size(cue)), ('cue_description','a10',np.size(cue_description)),('cue_type','a10',np.size(cue_type)), ('events','i4',(np.size(events,0),np.size(events,1)))])
    

    paradigm['start_delay'] = start_delay
    paradigm['isi_random'] = isi_random
    paradigm['cue'] = cue
    paradigm['cue_description'] = cue_description
    paradigm['cue_type'] = cue_type
    paradigm['events'] = events
    #% we have n events for which we store the event number, e.g. 1,2,3 etc and sample index
    cl = np.tile((np.arange(1., (nc)+1)+1.), (n, 1.))
    ev = cl.flatten(1)
    ev = ev[np.random.permutation(int(nc*n))-1]
    ev = ev.reshape(int(n), int(nc),order = 'F').copy()

    #% random mixture of left and right cues
    a = np.empty((int(n),0),int)
    for i in np.arange(1., int(nc)+1):
        ending = np.dot(np.ones((n,1)), nc)+2.
        middle = np.vstack((ev[:,int(i)-1]))
        front = np.ones((n,1))
        a = np.array(np.hstack((a,front,middle , ending)))
        

    ev = a.conj().T
    #% always put a rest in front of an event
    paradigm['events'][0][:,0] = ev.flatten(1)
    #% set event numbers
    nsub = np.size(sub_cue)
    if nsub > 1.:
        cc = np.hstack(('+'))
        cd = np.array(np.hstack(('rest',)))
        ct = np.hstack(('start_trial',))
       
        for i in np.arange(2., (np.size(cue))):
            for j in np.arange(1., (np.size(sub_cue))+1):
                cc = np.append(cc, cue[int(i)-1]+ ':'+ sub_cue[int(j)-1])
                cd = np.append(cd, cue_description[int(i)-1] + ':'+sub_cue[int(j)-1])
                ct = np.append(ct, cue_type[int(i)-1]+ ':'+ sub_cue_type[int(j)-1])
        
        cc[int(np.size(cc))-1] = ' '
        cd[int((np.size(cd)-1)+1.)-1] = 'ISI'
        ct[int((np.size(ct)-1)+1.)-1] = 'ISI'
        # paradigm['cue'] = cc
        # paradigm['cue_description'] = cd
        # paradigm['cue_type'] = ct
        # ev = paradigm['events']
        # evn = np.zeros((np.dot(n, nc)*3.+np.dot(np.dot(n, nc), nsub-1.)), 1.)
        # evn[0:matcompat.size[int(evn)-1,0]:nsub+2.] = 1.
        # evn[int(nsub+2.)-1:matcompat.size[int(evn)-1,0]:nsub+2.] = np.dot(nc, nsub)+2.
        # for i in np.arange(1., (nsub)+1):
        #     endPoint = matcompat.size[int(evn)-1,0]
        #     rangeTemp = arange(0,endPoint,int(nsub+2.))
        #     logicalTemp = int((ev > 1. and ev < (nc+2.)))
        #     evn[rangeTemp+i] = np.dot(ev[logicalTemp-1]-2., nsub)+i+1.
            
        # nc = np.dot(nsub, nc)
        # paradigm.events = np.zeros(matcompat.size(evn, 1.), 2.)
        # paradigm.events[:,0] = evn
        # ev = evn
    
    print np.size(paradigm['events'][0][:,0])
    callback_time = ncallback/fs
    time = np.round(paradigm['start_delay']/callback_time)
    cbtimes = np.zeros((np.size(paradigm['events'][0][:,0]), 1.))
    for i in np.arange(1., np.size(paradigm['events'][0][:,0])):
        cbtimes[int(i)-1] = int(time)
        #print i#paradigm['events'][0][i,0]
        _switch_val=paradigm['events'][0][int(i),0]
        if False: # switch 
            pass
        elif _switch_val == 1.:
            time = time+np.round(rest_interval/callback_time)
        elif _switch_val == nc+2.:
            tisi = 1.+np.random.randint(isi)
            time = time+np.round(tisi/callback_time)
        else:
            time = time+np.round(task_interval/callback_time)
        
    print cbtimes
    print np.size(cbtimes)
    cb_event = np.zeros((time, 2.))
    # temp = cbtimes - 1
    # cb_event[(cbtimes-1,1)] = 1.
    # cb_event[(cbtimes-1,0)] = ev.flatten(1)

    evTemp = ev.flatten(1)
    for ii in np.arange(1., np.size(cbtimes)):
        print cbtimes[int(ii)]
        cb_event[int(cbtimes[int(ii)])-1,1] = 1.
        cb_event[int(cbtimes[int(ii)])-1,0] = evTemp[ii]
    return [paradigm]

def process_event_emg(task, event, runIndex, totalTaskTime, sessionNumber):

    # Local Variables: runIndex, task, val, totalTaskTime, sessionNumber, record_length, ix0, event
    # Function calls: disp, set, process_event_emg, min, char, str2double, strfind, strcmp
    #% handle events for this paradigm
    _switch_val=task.cue_type[int(event)-1]
    if False: # switch 
        pass
    elif _switch_val == 'start_trial':
        set((task.bar), 'Visible', 'off')
        #%         set(task.text,'String',task.cue{event});
        set((task.text), 'String', 'Prepare')
        if strcmp(np.char((task.cue_type[1])), 'text:bar'):
            record_length = 10.
        else:
            record_length = totalTaskTime
            
        
        #%[status,cmdout] = system('record_length');
        #%         [status,cmdout] = system(char(trial_data));
        #%         current_time = num2str(clock);
        #%         for ii = length(current_time)
        #%             ending = strcat(ending,'-',current_time(ii))
        #%         end
        #%         dataFileName = ['emg_trial_' num2str(trialIndex) '_' ending '.dat'];
        #%         [status,cmdout] = system(dataFileName);
    elif _switch_val == 'ISI':
        set((task.bar), 'Visible', 'off')
        set((task.text), 'String', 'ISI')
    elif _switch_val == 'text':
        set((task.text), 'String', (task.cue.cell[int(event)-1]))
        set((task.bar), 'Visible', 'off')
    elif _switch_val == 'text:bar':
        ix0 = strfind((task.cue.cell[int(event)-1]), ':')
        val = str2double((task.cue.cell[int(event)-1,int(ix0+1.)-1:]()))/100.
        val = matcompat.max(val, 0.9)
        set((task.text), 'String', (task.cue.cell[int(event)-1]))
        if strfind((task.cue.cell[int(event)-1]), 'Left'):
            set((task.bar), 'Position', np.array(np.hstack((-val-.1, -.1, val, .2))), 'FaceColor', 'g', 'Visible', 'on')
        
        
        if strfind((task.cue.cell[int(event)-1]), 'Right'):
            set((task.bar), 'Position', np.array(np.hstack((.1, -.1, val, .2))), 'FaceColor', 'r', 'Visible', 'on')
        
        
    elif _switch_val == 'audio':
        np.disp('play audio here')
    
    return 

plt.close('all')
#%create_paradigm_reach(n,task_interval,rest_interval,isi,ncallback,fs,cue,sub_cue,cue_description,cue_type,sub_cue_type)
#%task=create_paradigm_reach(25,2,2,3,1200,1200,{'left','right'},{'25','50','75','100'},{'left graded','right graded'},{'text','text'},{'bar','bar','bar','bar'});

task = create_paradigm_reach(numOfTasks, taskInterval, restInterval, isiInterval, nCallBack, fs, cue, sub_cue, cue_description, cue_type, sub_cue_type)
runIndex = 0.
textStr = 'Initiating Trial...'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.00, 0.6, textStr, transform=ax.transAxes, fontsize=50, verticalalignment='top', bbox=props)

for i in np.arange(1., (np.size((cb_event)))+1):
    event = cb_event[int(i)-1,0]
    if event > 0.:
        if cue_type[int(event)-1] == 'start_trial':
            runIndex = runIndex+1.
            fID = fopen( 'emg_session_' + num2str(sessionNumber) + '.hdr'), 'a')
            if strcmp(np.char((task.cue.cell[int((task.cb_event[int((i+2.))-1,0]))-1])), np.char((task.cue.cell[1]))):
                trialData = np.char((task.cue[1]))
            else:
                trialData = np.char((task.cue[2]))
            
            fprintf(fID, '%d,%s,%s\n', runIndex, trialData, datestr(now, 'yyyy-mm-dd-HH-MM-SS'))
            fclose(fID)
        
        
        process_event_emg(task, event, runIndex, (taskInterval+restInterval), sessionNumber)
    
    pause(1.)

textStr = 'Ending Trial...'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.00, 0.6, textStr, transform=ax.transAxes, fontsize=50, verticalalignment='top', bbox=props)