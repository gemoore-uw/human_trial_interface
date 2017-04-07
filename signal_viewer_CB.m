function signal_viewer_CB(object,event,my_plot)

n =object.SamplesAcquiredFcnCount;
data=getdata(object,n);
add_data(my_plot,data);
