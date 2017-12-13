clear all
y_init = [0; 0];

dt = 0.01 ;

dac_u_set = [];
dac_x_set = [];
dac_dot_x_set = [];
% change the freq of the input seq
for freq = 1:1
    y_cur = y_init;
    %y_item_set for every individual y set for the freq
    y_item_set = [];
    u_set = [];
    u_item = wgn(200, 1, 0.05);
    for i = 1:200
        y_next = sim_sys(y_cur, dt, u_item(i, :));
        u_set = [u_set; u_item(i, :)];
        y_item_set = [y_item_set;y_next];
        y_cur = y_next;
    end
    dac_dot_x = diff(y_item_set)*100;
    dac_u = u_set(1:end-1, :)
    dac_x = y_item_set(1:end-1, :);
    
    dac_dot_x_set = [dac_dot_x_set; dac_dot_x];
    dac_x_set = [dac_x_set; dac_x];
    dac_u_set = [dac_u_set; dac_u];
end
%save('mimo_data_for_sindy', 'u_set', 'x', 'dot_x')
data = [dac_x_set dac_u_set dac_dot_x_set];
csvwrite('danbai_for_sindy.csv', data)
%plot(dac_goal_set)

