origin_x = 2;
origin_y = 2;

theta = 0;
dot_theta = 0;
dot_dot_theta = 0;

theta_set = [];
theta_dot_set = [];
theta_acc_set = [];
u_set = [];

dt = 0.01;

for i = 1:1000
    u =   3*sin(i/10);
    u_set = [u_set u];
    
    dot_dot_theta = - 10/1 * sin(theta) - 0.8 * dot_theta + u;
   
    dot_theta = dot_theta + dt*dot_dot_theta;
    
    theta = theta +  dt * dot_theta;
    
    theta_set = [theta_set theta];
    theta_dot_set = [theta_dot_set dot_theta];
    theta_acc_set = [theta_acc_set dot_dot_theta];
    
    if abs(dot_theta) < 0.01 && abs(dot_dot_theta) < 0.01
        break
    end
    x = 2 + 0.8*sin(theta); 
    y = 2 - 0.8*cos(theta);
    clf
    line([2, x], [2, y])
    hold on
    plot(x, y, '*')
    set(gca, 'XLim', [1 3]);
    set(gca, 'YLim', [.6 2]);
    
    %pause(0.009)
    i
    
    [theta dot_theta dot_dot_theta];
end
dac_goal = [theta_dot_set' theta_acc_set' - u_set'];
dac_input = [theta_set' theta_dot_set'];


