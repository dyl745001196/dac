close all 

%here we want to gather the data with different freq input like what we do
%in the freqency analysis in si.
dac_goal_whole_set = [];
dac_input_whole_set = [];

for index = 1:10
    init_value = 1;
    freq = index;
    [dac_goal, dac_input] = dac_setup(freq, [0:0.01:10], init_value);
    subplot(3, 4, index)
    plot(dac_goal, 'b');
    hold on 
    plot(dac_input', 'r')
    %legend('dac\_goal to do the si', 'dac\_input to do the si');
    grid on
    title(['u=sin(' int2str(index) '*t)'])
    xlabel('time step')
    ylabel('value')
    dac_goal_whole_set = [dac_goal_whole_set; dac_goal];
    dac_input_whole_set = [dac_input_whole_set; dac_input];
end


save('si_dac_data', 'dac_goal_whole_set', 'dac_input_whole_set')