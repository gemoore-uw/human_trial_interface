amplifier={'UA-2008.12.04'};

fprintf('getting hardware info from amps....');
daq_info=daqhwinfo('guadaq');
fs=1200;
f1=30;f2=550;fo=4; % display filter f1= lower corner freq, f2=upper corner freq, fo=filter order

my_settings=signal_viewer_class();
my_settings.message='callback';
my_settings.filterOn='on'; % set to not on for turning the filter off
my_settings.filterState=[];
[my_settings.filterB,my_settings.filterA]=butter(fo,[f1/fs f2/fs]*2);
my_settings.fs=fs;
my_settings.buffer_length=10; %10 s to show
my_settings.channel_sel=[[1 -1 0 0 0 0 0 0 0 0 0 0 0 0 0 0];[0 -1 1 0 0 0 0 0 0 0 0 0 0 0 0 0]]';% select a channel combination for each display channel
my_settings.channel_sel=eye(16); % all 16 monopolar
my_settings.channelChoice=1:2; % set of channels to display
my_settings.buffer=zeros(my_settings.buffer_length*fs,size(my_settings.channel_sel,2));
my_settings.t=(1:size(my_settings.buffer,1))'/my_settings.fs;
my_settings.fig=figure;hold on;
my_settings.ylim=[-100 100]*1e-6; % y-scale of the display in [V]
plot_buffer(my_settings);

my_settings.fig2=figure;
my_settings.spectChannel=1;
my_settings.showSpectro='on'; % show the spectrogram
my_settings.fr=1:10:500; % spectrogram frequencies 
my_settings.swindow=hann(256); % spectro fft window function
[S,F,T] = spectrogram(my_settings.buffer(:,my_settings.spectChannel),my_settings.swindow,220,my_settings.fr,my_settings.fs);
my_settings.spectroImag=imagesc(T,F,abs(S).^2);axis xy
my_settings.spectRange=[0 1e-5]; % display scale of the spectrogram
caxis(my_settings.spectRange);
dev_order=[2 1 3 4];dev_order=1:4;
common_Ground={'Enabled','Disabled'};
common_Reference={'Enabled','Disabled'};
gsel=1;rsel=1;
for i =1:length(daq_info.InstalledBoardIds)
    
    %order(i) = ceil(findstr(reshape(device_list', 1, []), ...
    %BCI.Setup.USBAmp.Id{i})/size(device_list,2));
    
    ain(i) = analoginput('guadaq',daq_info.InstalledBoardIds{dev_order(i)});
    ain(i).SampleRate = fs; % set the desired sampling rate
    ain(i).BufferingMode ='Auto'; % set buffersize to 60 m
    ain(i).SamplesPerTrigger = inf;    % never stop taking samples
    ain(i).LoggingMode = 'Memory'; % only memory
    ain(i).SlaveMode = 'on';
    
    addchannel(ain(i),1:16);% no trigger channel
    
    for ch=1:16
        set(ain(i).Channel(ch), 'NotchIndex', 9); % notch for 1200 Hz at 60 Hz
        set(ain(i).Channel(ch), 'BPIndex',116); % highpass at 2 Hz for 1200 HZ SR
    end
    set(ain(i),'GroupAToCommonGround',common_Ground{gsel},'GroupAToCommonReference',common_Reference{rsel});% set A group to common ref and ground
    set(ain(i),'GroupBToCommonGround',common_Ground{gsel},'GroupBToCommonReference',common_Reference{rsel});% set B group to common ref and ground
    set(ain(i),'GroupCToCommonGround',common_Ground{gsel},'GroupCToCommonReference',common_Reference{rsel});% set C group to common ref and ground
    set(ain(i),'GroupDToCommonGround',common_Ground{gsel},'GroupDToCommonReference',common_Reference{rsel});% set D group to common ref and ground
end
ain(end).SlaveMode = 'off'; % master device. Assume that master device is the highest device serial
ain(end).SamplesAcquiredFcnCount = ceil(fs/20); % update 20x per second 

ain(end).SamplesAcquiredFcn ={@signal_viewer_CB,my_settings};
fprintf('done\n');