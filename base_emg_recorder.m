
function record_data_qeeg(command,fname)

global BCI

if nargin < 2
    fname = 'dummy';
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
switch command
    case 'init'
        loc_init(fname);
    case 'start'
        loc_start;
    case 'stop'
        loc_stop;
    case 'cleanup'
        loc_cleanup;
    case 'daq_cb'
        loc_daqcallback;
    case 'daq_stop'
        loc_stop_cb;
    otherwise
        error('invalid command');
end

if BCI.StopExecution == 1
    loc_stop;
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function loc_init(fname)

global BCI

BCI.config=1;

BCI.Setup.Fs=4800; % set samplingrate to 4800 Hz
BCI.Setup.BufSize = 60e-3; % internal thing

%BCI.Setup.USBAmp.Id ={'UA-2008.12.19','UA-2008.12.04','UA-2007.02.15','UA-2007.02.14'};    % serial of amps, master is last
if BCI.config==1
    BCI.Setup.USBAmp.Id ={'UA-2008.12.04'}; % make sure the LAST amplifier in the list is the master
    BCI.Setup.USBAmp.ChannelList = {1:17};
    BCI.Setup.USBAmp.GroupToCommonGround    = {[1 1 1 1]};
    BCI.Setup.USBAmp.GroupToCommonReference = {[1 1 1 1]};
end
if BCI.config==2
    BCI.Setup.USBAmp.Id ={'UA-2008.12.04','UA-2008.12.19'}; % make sure the LAST amplifier in the list is the master
    BCI.Setup.USBAmp.ChannelList = [{1:17}, {1:17}];
    BCI.Setup.USBAmp.GroupToCommonGround    = [{[0 0 0 0]}, {[0 0 0 0]}];
    BCI.Setup.USBAmp.GroupToCommonReference = [{[0 0 0 0]}, {[0 0 0 0]}];
end
if BCI.config==4
 BCI.Setup.USBAmp.Id ={'UA-2007.04.06','UA-2007.04.07','UA-2008.12.04','UA-2008.12.19'};  
 BCI.Setup.USBAmp.ChannelList = [{1:17}, {1:17},{1:17},{1:17}];
 BCI.Setup.USBAmp.GroupToCommonGround    = [{[0 0 0 0]}, {[0 0 0 0]},{[0 0 0 0]}, {[0 0 0 0]}];
 BCI.Setup.USBAmp.GroupToCommonReference = [{[0 0 0 0]}, {[0 0 0 0]}, {[0 0 0 0]}, {[0 0 0 0]}];
end % serial of amps, master is last

% for sub-cutaneous recording SEPARATE blocks for all electrodes. Make sure
% to link ground and reference PHYSCIALLY if using more than 4 electrodes


BCI.FileName = fname;

%% see check_amp_order to generate the file
BCI.StopExecution = 0;


%% initialize amps
order = [];
no_channels = 0;
clear ain;
fprintf('getting hardware info from amps....');
daq_info=daqhwinfo('guadaq');
fprintf('done\n');

fprintf('initalizing....');

for i = 1:length(BCI.Setup.USBAmp.Id),

    %order(i) = ceil(findstr(reshape(device_list', 1, []), ...
    %BCI.Setup.USBAmp.Id{i})/size(device_list,2));

    ain(i) = analoginput('guadaq',daq_info.InstalledBoardIds{i});
    ain(i).SampleRate = BCI.Setup.Fs; % set the desired sampling rate
    ain(i).BufferingMode ='Auto'; % set buffersize to 60 m
    ain(i).SamplesPerTrigger = inf;    % never stop taking samples
    ain(i).LoggingMode = 'Disk&Memory'; % store session data on the disk
    ain(i).LogFileName = sprintf('%s_%s.daq',BCI.FileName, ain(i).DeviceSerial);
    ain(i).SlaveMode = 'on';

    addchannel(ain(i),BCI.Setup.USBAmp.ChannelList{i});

    if (0) % no filters
        for ch=BCI.Setup.USBAmp.ChannelList{i}
            if ch < 17
                set(ain(i).Channel(ch), 'BPIndex',116);
                set(ain(i).Channel(ch), 'NotchIndex', 9);
            end
            no_channels = no_channels+1;
        end
    end

   

    set(ain(i),'GroupAToCommonGround','Disabled','GroupAToCommonReference','Disabled');% set A group to common ref and ground
    set(ain(i),'GroupBToCommonGround','Disabled','GroupBToCommonReference','Disabled');% set B group to common ref and ground
    set(ain(i),'GroupCToCommonGround','Disabled','GroupCToCommonReference','Disabled');% set C group to common ref and ground
    set(ain(i),'GroupDToCommonGround','Disabled','GroupDToCommonReference','Disabled');% set D group to common ref and ground
end
fprintf('done\n');
order=1:length(BCI.Setup.USBAmp.Id);
for i = 1:length(BCI.Setup.USBAmp.Id),
    dev=ain(i).DeviceSerial;
    order(i)= find(strcmp(dev, BCI.Setup.USBAmp.Id));
end
ain=ain(order);
for i = 1:length(BCI.Setup.USBAmp.Id),
    
    if BCI.Setup.USBAmp.GroupToCommonGround{i}(1) == 1,
        set(ain(i),'GroupAToCommonGround','Enabled');
    else
        set(ain(i),'GroupAToCommonGround','Disabled');
    end
    if BCI.Setup.USBAmp.GroupToCommonGround{i}(2) == 1,
        set(ain(i),'GroupBToCommonGround','Enabled');
    else
        set(ain(i),'GroupBToCommonGround','Disabled');
    end
    if BCI.Setup.USBAmp.GroupToCommonGround{i}(3) == 1,
        set(ain(i),'GroupCToCommonGround','Enabled');
    else
        set(ain(i),'GroupCToCommonGround','Disabled');
    end
    if BCI.Setup.USBAmp.GroupToCommonGround{i}(4) == 1,
        set(ain(i),'GroupDToCommonGround','Enabled');
    else
        set(ain(i),'GroupDToCommonGround','Disabled');
    end
    
    if BCI.Setup.USBAmp.GroupToCommonReference{i}(1) == 1,
        set(ain(i),'GroupAToCommonReference','Enabled');
    else
        set(ain(i),'GroupAToCommonReference','Disabled');
    end
    if BCI.Setup.USBAmp.GroupToCommonReference{i}(2) == 1,
        set(ain(i),'GroupBToCommonReference','Enabled');
    else
        set(ain(i),'GroupBToCommonReference','Disabled');
    end
    if BCI.Setup.USBAmp.GroupToCommonReference{i}(3) == 1,
        set(ain(i),'GroupCToCommonReference','Enabled');
    else
        set(ain(i),'GroupCToCommonReference','Disabled');
    end
    if BCI.Setup.USBAmp.GroupToCommonReference{i}(4) == 1,
        set(ain(i),'GroupDToCommonReference','Enabled');
    else
        set(ain(i),'GroupDToCommonReference','Disabled');
    end
end
ain(end).SlaveMode = 'off'; % master device. Assume that master device is the highest device serial
%ain(end).SamplesAcquiredFcnCount = ceil(BCI.Setup.Fs/20); % 
ain(end).SamplesAcquiredFcnCount = ceil(BCI.Setup.Fs/1); % every second
ain(end).SamplesAcquiredFcn = 'base_emg_recorder(''daq_cb'')';
%ain(end).StopFcn = 'record_data(''daq_stop'')';

BCI.Setup.ain = ain;
BCI.StopExecution=0;

BCI.Paradigm.call_back_counter=0;
BCI.Paradigm.event_counter=0;

% base task - just wiggle
task=create_paradigm_reach(25,2,2,3,4800,4800,{'on'},{},{'only ear movement - any side'},{'text'});

% left/right up/down task
%diff_class_task=create_paradigm_reach(25,2,2,3,4800,4800,{'up left','up right','back left','back right'},{},{'left superior','right superior','left posterior','right posterior'},{'text','text','text','text'},{});

% artifact test
%task=create_paradigm_reach(15,2,2,3,4800,4800,{'jaw clench','eye movement','neck tension','talk'},{},{'artifact jaw','artifact eye','artifact neck','talk'},{'text','text','text','text'},{});
% graded left-right
%task=create_paradigm_reach(25,2,2,3,1200,1200,{'left','right'},{'25','50','75','100'},{'left graded','right graded'},{'text','text'},{'bar','bar','bar','bar'});


BCI.Paradigm.task=task;


BCI.Paradigm.task.photodiode=0;
BCI.Paradigm.Event_list=BCI.Paradigm.task.cb_event(:,1);

%BCI.Setup.ain.BufferingConfig
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function loc_start
global BCI
BCI.StopExecution =0;
start(BCI.Setup.ain);
disp('DAQ objects started');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function loc_stop
global BCI
BCI.StopExecution=1;

obj=BCI.Setup.ain(end);
if(isrunning(obj))
    stop(BCI.Setup.ain);
    fprintf('DAQ objects stopped\n');
end
save([BCI.FileName '_info'], 'BCI');
close all
beep

% if ~isempty(BCI.UDP.hCon)
%     pnet(BCI.UDP.hCon, 'close');
% end



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function loc_cleanup

global BCI
delete(BCI.Setup.ain);
daqreset;
disp('DAQ objects deleted. DAQ toolbox resetted.');


function loc_stop_cb
global BCI
obj=BCI.Setup.ain(end);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function loc_daqcallback
global BCI
% do nothing
obj=BCI.Setup.ain(end);
if BCI.StopExecution==0
    if(isrunning(obj))
        namp=length(BCI.Setup.ain);
        
        t = get(BCI.Setup.ain(end), 'SamplesAcquired');
        n = BCI.Setup.ain(end).SamplesAcquiredFcnCount;
        
        %     ni=zeros(namp,1);
        %     for i=1:namp
        %         n = BCI.Setup.ain(i).SamplesAcquiredFcnCount;
        %         nmax=BCI.Setup.ain(i).SamplesAvailable;
        %         ni(i)=min(n,nmax);
        %
        %     end
        %     n=min(ni)
        disp(sprintf('%i seconds acquired\n',round(t/BCI.Setup.Fs)))
        %% spatial filtering
        %d=zeros(n,nchan*namp);
        achan=zeros(namp,1);
        nchan=0;
        for i=1:namp
            nchan=nchan+length(BCI.Setup.ain(i).Channel);
            achan(i)=length(BCI.Setup.ain(i).Channel);
        end
        d=zeros(n,nchan);
        cc=1;
        for i=1:namp
            ix=(cc):(cc+achan(i)-1);
            d(:,ix)=getdata(BCI.Setup.ain(i),n);
            cc=cc+achan(i);
        end
        BCI.Paradigm.call_back_counter=BCI.Paradigm.call_back_counter+1; % count callbacks
        if ~isempty(BCI.Paradigm.Event_list)
            %process some events
            if BCI.Paradigm.call_back_counter<=length(BCI.Paradigm.Event_list)
                event=BCI.Paradigm.Event_list(BCI.Paradigm.call_back_counter,1);
                if(event>0)
                    % process event
                    %fprintf('event = %i\n',event)
                    BCI.Paradigm.event_counter=BCI.Paradigm.event_counter+1;
                    process_event_emg(BCI.Paradigm.task,event);
                    BCI.Paradigm.task.events(BCI.Paradigm.event_counter,2)=obj.SamplesAcquired;
                end
            else
                %stop
                BCI.StopExecution=1;
            end
        end
    end
else
    obj=BCI.Setup.ain(end);
    if(isrunning(obj))
        stop(BCI.Setup.ain);
        disp('DAQ objects stopped');
    end
    save([BCI.FileName '_info'], 'BCI');
    close all
    beep
end

