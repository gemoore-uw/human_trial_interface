
import numpy as np
import scipy
import matcompat

# import numpy
# if available import pylab (from matlibplot)
try:
    import matplotlib.pylab as plt
    import matplotlib.patches as patches
except ImportError:
    print 'import matplotlib error'
    pass

# try:
#     import numpy.lib.recfunctions import append_fields
# except ImportError:
#     print 'import append fields error'
#     pass

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