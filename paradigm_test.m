% FILE: paradigm_test.m
% DESCRIPTION: Client program for running the human trial interface.

close all; % close all windows
%create_paradigm_reach(n,task_interval,rest_interval,isi,ncallback,fs,cue,sub_cue,cue_description,cue_type,sub_cue_type)
%task=create_paradigm_reach(25,2,2,3,1200,1200,{'left','right'},{'25','50','75','100'},{'left graded','right graded'},{'text','text'},{'bar','bar','bar','bar'});

sessionNumber = 1; % session number

numOfTasks = 5;    % number of tasks of each cue
taskInterval = 2;  % number of seconds for the task
restInterval = 2;  % number of seconds before the task for restperiod
isiInterval = 4;   % inter stimulus interval
nCallBack = 1200;  % number of samples after which callback is called
fs = 1200;         % sampling rate
cue = {'Left','Rest'}; % list of cues
cue_type = {'text', 'text'}; % type of each cue (ex: 'text','audio', etc)
sub_cue = {''};%{'25','50','75','100'}; %  % list of percent flex
cue_description = {'left flex','rest'}; % description of each cue
sub_cue_type = {'bar','bar','bar','bar'}; % ???

% creates the paradigm for a cued hand movement
task = create_paradigm_reach(numOfTasks,taskInterval,restInterval,isiInterval,nCallBack,fs,cue,sub_cue,cue_description,cue_type,sub_cue_type);

runIndex = 0; % index of each run of an event
set(task.text,'String','Initiating Trial...'); % display 'Initiating Trial'
for i = 1:size(task.cb_event,1) % loop through each event type
    event = task.cb_event(i,1); % set event to number representing the cue (0-4)
    % 0=no change, 1=prepare, 2=left, 3=rest, 4=ISI)
    if event > 0 % if event type is greater than 0
        if strcmp(task.cue_type{event}, 'start_trial') % if event type = 'start_trial' (first loop)
            runIndex = runIndex + 1; % increase runIndex by 1
            fID = fopen(strcat('emg_session_', num2str(sessionNumber), '.hdr'), 'a'); % create file (ex: emg_session_1.hdr)
            
            if strcmp(char(task.cue{task.cb_event(i+2,1)}),char(task.cue{2})) % if task.cue (at 2 indices after the current index) = 'Left'                 
            	trialData = char(task.cue(2)); % sets trialData to 'Left'
            else
                trialData = char(task.cue(3)); % else: sets trialData to 'Rest'
            end
            
            % prints a line to fID file (ex: 6,Rest,2017-03-29-12-40-19)
            fprintf(fID, '%d,%s,%s\n',  runIndex, trialData, datestr(now,'yyyy-mm-dd-HH-MM-SS'));
            fclose(fID); % closes the file
        end
        
        % processes the current event
        process_event_emg(task,event, runIndex,taskInterval+restInterval,sessionNumber);
    end
    pause(1) % pause for 1 second
end

set(task.text,'String','Ending Trial...'); % display 'Ending Trial...'
