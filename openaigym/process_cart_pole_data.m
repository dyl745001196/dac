load('episodes.mat');
dac_goal_set = [];
dac_input_set =[];
for i = 1:200
    data = episodes(1, i);
    data = cell2mat(data);
    theta = data(:, 3);
    dot_theta = data(:, 4);
    dot_dot_theta = diff(dot_theta)  ;


    scale1 = 5;
    scale2 = 1/2;
    scale3 = 3;




    scale_theta = theta(1:end-1)*scale1;
    scale_dot_theta = dot_theta(1:end-1)*scale2 ;
    scale_dot_dot_theta = dot_dot_theta*scale3;

    u = data(:, 5);


    plot(scale_theta, 'b');
    hold on
    plot(scale_dot_theta, 'g');
    hold on
    plot(scale_dot_dot_theta, 'r');
    hold on
    plot(u, 'k')
    u = 2*u(1:end-1) - 1;
    u = [zeros(size(u)) u/20];


    dac_goal = [scale_dot_theta scale_dot_dot_theta] ;
    dac_input = [scale_theta scale_dot_theta];

    dac_goal_set = [dac_goal_set; dac_goal];
    dac_input_set = [dac_input_set ; dac_input];
end

dac_goal = dac_goal_set;
dac_input = dac_input_set;
save('../test.mat', 'dac_goal', 'dac_input');
