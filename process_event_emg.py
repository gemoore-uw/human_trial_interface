
import numpy as np
import scipy
import matcompat

# if available import pylab (from matlibplot)
try:
    import matplotlib.pylab as plt
except ImportError:
    pass

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