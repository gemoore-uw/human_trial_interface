% FILE: process_event_emg.m
% DESCRIPTION: Handles events for this paradigm by displaying the current cue.

function process_event_emg(task, event, runIndex, totalTaskTime, sessionNumber)
    % task = result from create_paradigm_reach.m
    % event = number representing the cue (0-4) where 0=no change, 1=prepare, 2=left, 3=rest, 4=ISI)
    % runIndex = index of each run of an event
    % totalTaskTime = number of seconds for the task + number of seconds before the task for restperiod
    % sessionNumber = session number
    
    switch task.cue_type{event}
        case 'start_trial' % cue type is 'start_trial'
            set(task.bar,'Visible','off');
    %       set(task.text,'String',task.cue{event});
            set(task.text,'String','Prepare'); % display 'Prepare'
            if(strcmp(char(task.cue_type(2)), 'text:bar')) % if 'text' = 'text:bar' ???
                record_length = 10; % set record_length to 10
            else
                record_length = totalTaskTime; % set record_length to totalTaskTime
            end
    %         [status,cmdout] = system('record_length');
    %         [status,cmdout] = system(char(trial_data));
    %         current_time = num2str(clock);
    %         for ii = length(current_time)
    %             ending = strcat(ending,'-',current_time(ii))
    %         end
    %         dataFileName = ['emg_trial_' num2str(trialIndex) '_' ending '.dat'];
    %         [status,cmdout] = system(dataFileName);
    
        case 'ISI' % cue type is 'ISI'
            set(task.bar,'Visible','off');
            set(task.text,'String','ISI'); % display ISI
            
        case 'text' % cue type is 'text'
            set(task.text,'String',task.cue{event}); % display cue (ex: 'left')
            set(task.bar,'Visible','off');
            
        case 'text:bar' % cue type is 'text:bar' ???
            ix0 = strfind(task.cue{event},':'); % sets ix0 to the index of ':' in task.cue
            val = str2double(task.cue{event}(ix0+1:end))/100; % sets val to a double
            val = min(val,0.9); % sets val to the minimum of val and 0.9
            set(task.text,'String',task.cue{event}); % display cue of the current event
            if strfind(task.cue{event},'Left') % if cue is 'Left'
                set(task.bar,'Position',[-val-.1,-.1,val,.2],'FaceColor','g','Visible','on')
            end

            if strfind(task.cue{event},'Right') % if cue is 'Right'
                set(task.bar,'Position',[.1,-.1,val,.2],'FaceColor','r','Visible','on')
            end

        case 'audio' % cue type is 'audio' ???
            disp('play audio here') % displays 'play audio here'
end