y_init = [0; 0];

dt = 0.01 ;

dac_goal_set = [];
dac_input_set = [];
% change the freq of the input seq
for freq = 1:5
    y_cur = y_init;
    %y_item_set for every individual y set for the freq
    y_item_set = [];
    u_set = [];
    for i = 1:200
        y_next = sim_sys(y_cur, dt, [0.8*sin(freq*i/20); 0.6*sin(freq*i/20)]);
        u_set = [u_set; [0.8*sin(freq*i/20) 0.6*sin(freq*i/20)]];
        y_item_set = [y_item_set;y_next];
        y_cur = y_next;
    end
    diff_y_item = diff(y_item_set)*100;
    dac_goal = diff_y_item - u_set(1:end-1, :);
    dac_input = y_item_set(1:end-1, :);
    
    dac_goal_set = [dac_goal_set; dac_goal];
    dac_input_set = [dac_input_set; dac_input];
end
save('mimo_data', 'dac_goal_set', 'dac_input_set')

plot(dac_goal_set)

