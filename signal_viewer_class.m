classdef signal_viewer_class < handle
    properties
        message='';
        fs;
        buffer_length;  
        channel_sel;
        buffer;
        t;
        fr;
        fig;
        fig2;
        buffer_plot;
        ylim;
        filterState;
        filterA;
        filterB;
        filterOn;
        channelChoice;
        spectChannel;
        showSpectro;
        spectroImag;
        spectRange;
        swindow;
    end
    
    methods
        function plot_buffer(self)
            figure(self.fig);
            for i=1:length(self.buffer_plot)
                delete(self.buffer_plot(i))
            end
            self.buffer_plot=[];
            for i=1:length(self.channelChoice)
                self.buffer_plot(i)=plot(self.t,self.buffer(:,self.channelChoice(i))+diff(self.ylim)*1.1*(i-1));
            end
            ylim([self.ylim(1) diff(self.ylim)*length(self.channelChoice)+self.ylim(1)])
        end
        function compute_spectrum(self)
            
        end
        function add_data(self,data)
            n=size(data,1);
            dataf=data;
            if strcmp(self.filterOn,'on')
                [dataf,self.filterState]=filter(self.filterB,self.filterA,data,self.filterState);
            end
            y=dataf*self.channel_sel;
            self.buffer=circshift(self.buffer,-n);
            t0=self.t(end);
            self.t=circshift(self.t,-n);
            self.buffer(end-n+1:end,:)=y;
            self.t(end-n+1:end)=t0+(1:n)/self.fs;
            if length(self.buffer_plot)~=length(self.channelChoice)
                plot_buffer(self)
            end
            for i=1:length(self.channelChoice)
                set(self.buffer_plot(i),'XData',self.t,'YData',self.buffer(:,self.channelChoice(i))+diff(self.ylim)*1.1*(i-1));
                p=get(self.buffer_plot(i),'Parent');
                set(p,'XLim',[min(self.t) max(self.t)]);
            end
            ylim([self.ylim(1) diff(self.ylim)*length(self.channelChoice)+self.ylim(1)])
            if strcmp(self.showSpectro,'on')
                
                S = spectrogram(self.buffer(:,self.spectChannel),self.swindow,220,self.fr,self.fs);
                set(self.spectroImag,'CData',abs(S).^2);
                set(self.spectroImag,'XData',self.t);
                caxis(self.spectRange);
                p=get(self.spectroImag,'Parent');
                set(p,'XLim',[min(self.t) max(self.t)]);
                set(p,'YLim',[min(self.fr) max(self.fr)]);
            end
        end
    end
end
