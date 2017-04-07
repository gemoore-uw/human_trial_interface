close all;
%create_paradigm_reach(n,task_interval,rest_interval,isi,ncallback,fs,cue,sub_cue,cue_description,cue_type,sub_cue_type)
%task=create_paradigm_reach(25,2,2,3,1200,1200,{'left','right'},{'25','50','75','100'},{'left graded','right graded'},{'text','text'},{'bar','bar','bar','bar'});

sessionNumber = 1;

numOfTasks = 5;    %this is numOfTasks of each cue
taskInterval = 2;
restInterval = 2;
isiInterval = 4;
nCallBack = 1200;
fs = 1200;
cue = {'Right','Rest'};
sub_cue = {''};%{'25','50','75','100'};
cue_description = {'left flex','rest'};
cue_type = {'text','text'};
sub_cue_type = {'bar','bar','bar','bar'};

cmd ='echo ee359 | sudo -kS';
system(cmd)
cmd ='su';
system(cmd)

system('exit')

source /home/sensor/prefix/october_2016/setup_env.sh
python /home/sensor/EMG-analog-backscatter/top_block_x300_emg_human_trial.py


[status, cmdout] = system(cmd)
% cmd = ' /home/sensor/EMG-analog-backscatter'
% [status, cmdout] = system(cmd)
% cmd = 'ls'
% [status, cmdout] = system(cmd)
cmd ='echo ee359 | sudo -kS';
system(cmd)
cmd ='su';
system(cmd)
cmd = python /home/sensor/EMG-analog-backscatter/top_block_x300_emg_human_trial.py
system(python /home/sensor/EMG-analog-backscatter/top_block_x300_emg_human_trial.py)

python /home/sensor/EMG-analog-backscatter/top_block_x300_emg_human_trial.py

task=create_paradigm_reach(numOfTasks,taskInterval,restInterval,isiInterval,nCallBack,fs,cue,sub_cue,cue_description,cue_type,sub_cue_type);

runIndex = 0;
set(task.text,'String','Initiating Trial...');
for i=1:size(task.cb_event,1)
    event=task.cb_event(i,1);
    if event>0
        if(strcmp(task.cue_type{event}, 'start_trial'))
            runIndex = runIndex+1;
            fID = fopen(['emg_session_', num2str(sessionNumber), '.hdr'], 'a');
            if(strcmp(char(task.cue{task.cb_event(i+2,1)}),char(task.cue{2})))                
            	trialData = char(task.cue(2));
            else
                trialData = char(task.cue(3));
            end
            fprintf(fID, '%d,%s,%s\n',  runIndex, trialData, datestr(now,'yyyy-mm-dd-HH-MM-SS'));
            fclose(fID);
        end
        process_event_emg(task,event, runIndex,taskInterval+restInterval,sessionNumber);
    end
    pause(1)
end

set(task.text,'String','Ending Trial...');