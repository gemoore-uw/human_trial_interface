% FILE: create_paradigm_reach.m
% DESCRIPTION: Creates the paradigm for a cued hand movement.

function paradigm = create_paradigm_reach(n,task_interval,rest_interval,isi,ncallback,fs,cue,sub_cue,cue_description,cue_type,sub_cue_type)

    % n = number of tasks
    % task_interval = number of seconds for the task
    % rest_interval = number of seconds before the task for restperiod
    % isi = inter stimulus interval 
    % ncallback = number of samples after which callback is called
    % fs = sampling rate
    % cue = list of cues
    % cue_description = description of what happens at each cue
    % cue_type = 'text','audio' etc
    % sub_cue_type

    paradigm.figure = figure('Position',[8.2 46.6 753 832]); % creates and opens figure window
    paradigm.text = text(0.00,0.0,'+','FontSize',60,'HorizontalAlignment','center'); % creates fixation cross at (0,0)
    %paradigm.text2=text(-0.50,0.0,'+','FontSize',60,'HorizontalAlignment','center'); % fixation cross

    paradigm.bar = rectangle('Position',[0,-.1,.1,.2],'FaceColor','b','Visible','off');
    xlim([-1 1]);ylim([-1 1]); % set axes to be between -1 and 1
    axis off % turns off the axes
%     paradigm.photodiode = 0; % sets photodiode to 0 ???
%     if(paradigm.photodiode) % if photodiode = 1
%         paradigm.marker = rectangle('position',[-1 -1 .1 .1],'FaceColor',ones(1,3),'EdgeColor',ones(1,3));
%     end

    paradigm.start_delay = 5; % wait for 10s before actually doing something ???
    paradigm.isi_random = 1; % we want random ISI
    nc = size(cue,2); % number of columns in cue
    paradigm.cue = ['+',cue,' ']; % sets cue to a list of '+' followed by input list cue
    %paradigm.cue={'+','left','right',''}; % we have three cues
    paradigm.cue_description = ['rest',cue_description,'ISI']; % sets cue descriptions
    paradigm.cue_type=['start_trial', cue_type, 'ISI'];  % sets type of each cue

    prepareAndISIInclusion = 3;
    paradigm.events = zeros(n*nc*prepareAndISIInclusion,2);  % sets events to a n*nc*3 by 2 matrix (col vs row)
    % we have n events for which we store the event number, e.g. 1,2,3 etc and sample index
    cl = repmat((1:nc)+1,n,1); % n copies of matrix with row values 1 to 1+nc 
    ev = cl(:); % single column vector of cl
    ev = ev(randperm(nc*n));
    a = [ones(n*nc,1) ev ones(n*nc,1)*nc+2]; % matrix with column of ones, ev up to i, column of (nc+2)'s
    ev = a'; % always put a rest in front of an event (transposes a) not working???

    paradigm.events(:,1) = ev(:); % set event numbers
    nsub = size(sub_cue,2); % number of columns in sub_cue
    if nsub > 1 % for using graded flexing
        cc = {'+'};
        cd = {'rest'};
        ct = {'start_trial'};
        u = 2;
        for i = 1:size(cue,2) % loop through number of columns in cue
            for j = 1:size(sub_cue,2)  % loop through number of columns in sub_cue
                cc{u} = strcat(cue{i}, ':', sub_cue{j});             % ex: 'left:25'
                cd{u} = strcat(cue_description{i}, ':', sub_cue{j}); % ex: 'left_flex:25'
                ct{u} = strcat(cue_type{i}, ':', sub_cue_type{j});   % ex: 'text:bar'
                u = u+1;
            end
        end
        cc{size(cc,2)+1} = ' ';
        cd{size(cd,2)+1} = 'ISI';
        ct{size(ct,2)+1} = 'ISI';
        paradigm.cue = cc;
        paradigm.cue_description = cd;
        paradigm.cue_type = ct;
        ev = paradigm.events(:, 1);
        evn = zeros(n*nc*3 + n*nc*(nsub-1), 1);
        evn(1:(nsub+2):size(evn,1)) = 1;
        evn((nsub+2):(nsub+2):size(evn,1)) = nc*nsub+2;
        for i=1:nsub
            evn((1:(nsub+2):size(evn,1))+i) = (ev((ev>1) & (ev<(nc+2)))-2)*nsub+i+1;
        end
        nc = nsub*nc;
        paradigm.events = zeros(size(evn,1),2);
        paradigm.events(:,1) = evn;
        ev = evn;
    end
    callback_time = ncallback/fs; % computes time by number of samples / samples per second

    time = round(paradigm.start_delay/callback_time); % rounded start_delay / callback_time
    cbtimes = zeros(size(paradigm.events,1),1); % column vector with length of events # of rows
    for i = 1:size(paradigm.events,1)
        cbtimes(i) = time; % sets each element equal to time
        switch(paradigm.events(i,1)) % checks 1st row of events
            case 1 % events is 1
                time = time + round(rest_interval/callback_time);       
            case nc+2 % events is nc + 1
                tisi = 1 + randi(isi); % 1 + random integer up to isi
                time = time + round(tisi/callback_time);
            otherwise
                time = time + round(task_interval/callback_time);
        end
    end

    paradigm.cb_event = zeros(time,2); % time by 2 matrix of zeros
    paradigm.cb_event(cbtimes,2) = 1; % sets values (present in cbtimes) in the 2nd row of cb_event to 1 ???
    paradigm.cb_event(cbtimes,1) = ev(:); % sets values in the 1st row of cb_event to ev
    