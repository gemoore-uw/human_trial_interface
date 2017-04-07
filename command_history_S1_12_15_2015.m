gUSBampImpedancep('UA-2008.12.04')
clear all
gUSBampImpedancep('UA-2008.12.04')
gUSBampImpedancep('UA-2008.12.04',1)
impedance=gUSBampImpedancep('UA-2008.12.04',1)
save  S1/impedance.mat impedance
clear all
close all
base_emg_recorder('init','S1\on_off_recording_1');
base_emg_recorder('start');
base_emg_recorder('stop');
clear all
base_emg_recorder('init','S1\on_off_recording_1');
base_emg_recorder('start');
clear all
base_emg_recorder('init','S1\on_off_recording_2');
base_emg_recorder('start');
clear all
base_emg_recorder('init','S1\artifact_run_1');
base_emg_recorder('start');
clear all
base_emg_recorder('init','S1\on_off_recording_3');
base_emg_recorder('start');
help butter
[b60,a60]=cheby2(N,R,[59 61]/fs*2,'stop');
[b120,a120]=cheby2(N,R,[119 121]/fs*2,'stop');
cheby2(N,R,Wst,'stop')
fs=1200
R=20;N=4;
[b60,a60]=cheby2(N,R,[59 61]/fs*2,'stop');
[b120,a120]=cheby2(N,R,[119 121]/fs*2,'stop');
freqz(b60,a60,1024,1200)
bnd=60:60:600
length(bnd)
b60Hz=cell(10,1);a60Hz=cell(10,1);
for bnd=1:1:10
[b60{bnd},a60{bnd}]=cheby2(N,R,[59+(bnd-1)*60 61+(bnd-1)*60]/fs*2,'stop');
end
for bnd=1:1:10
[b60Hz{bnd},a60Hz{bnd}]=cheby2(N,R,[59+(bnd-1)*60 61+(bnd-1)*60]/fs*2,'stop');
end
b60Hz=cell(9,1);a60Hz=cell(9,1);
for bnd=1:1:9
[b60Hz{bnd},a60Hz{bnd}]=cheby2(N,R,[59+(bnd-1)*60 61+(bnd-1)*60]/fs*2,'stop');
end
b60Hz
clear all
signal_viewer
start(ain)
my_settings.channelChoice=[5 7 6 8]
stop(ain)
plot_buffer(my_settings)
start(ain)
my_settings.showSpetro='off'
my_settings.showSpectro='off'