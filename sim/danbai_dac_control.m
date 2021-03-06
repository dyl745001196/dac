origin_x = 2;
origin_y = 2;

theta = 0;
dot_theta = 0;
dot_dot_theta = 0;



dt = 0.01;

x_cur = [theta dot_theta];
x_m_cur = [0 0];
x_set =[];
x_m_set = [];


T_const = 20;
%%%%%dac parameters 
k_x_hat = [-T_const 0;
            0 -T_const];
k_r_hat = [T_const 0;
           0 T_const];
 

gamma_x = [100 0;
           0 1];
gamma_r = [1 0
           0 100];
       
P = [1 0;
     0 1];     
phi_hat = [1 0;
             0 1];
phi = phi_hat;

for i = 1:50
     
    r = [(log(i/100) + 4.61)/10 10/i];
    DL_x_r = (offline_nn(x_cur)* phi_hat)' + k_x_hat * x_cur' + k_r_hat * r';
    
    dot_dot_theta = - 10/1 * sin(theta) - 0.8 * dot_theta + DL_x_r(2);
    dot_theta = dot_theta + dt*dot_dot_theta;
    theta = theta +  dt * dot_theta;
    
    x_next = [theta dot_theta];
    x_m_next = sim_ref(x_m_cur, dt, r);
    
    x_cur = x_next;
    x_m_cur = x_m_next;
    x_set = [x_set; x_cur];
    x_m_set = [x_m_set; x_m_cur];
    
    e = x_cur - x_m_cur;
    
    phi_hat = phi_hat -dt*gamma_x*x_cur'*e*P;
    k_x_hat = k_x_hat -dt*gamma_r*r'*e*P;
    k_r_hat = k_r_hat -dt*offline_nn(x_cur)'*e*P;
    
    x = 2 + 0.8*sin(theta); 
    y = 2 - 0.8*cos(theta);
    
    x_ref = 2 + 0.8*sin(r(1));
    y_ref = 2 - 0.8*cos(r(1));
    clf
    line([2, x], [2, y])
    hold on
    plot(x, y, '*')
    plot(x_ref, y_ref, 'r*')
    set(gca, 'XLim', [1 3]);
    set(gca, 'YLim', [.6 2]);
    
    pause(0.09)
end
figure
t_span = 1:50;
t_span = t_span /50;
subplot(2, 1, 1)
cla
plot(t_span, x_m_set(:, 1), '--r', 'LineWidth', 2)
hold on 
plot(t_span, x_set(:, 1), 'b', 'LineWidth', 2)
legend('ref system state x1', 'dac theta')
subplot(2, 1, 2)
cla
plot(t_span, x_set(:, 2), 'b', 'LineWidth', 2)
hold on 
plot(t_span, x_m_set(:, 2), '--r', 'LineWidth', 2)
legend('ref system state x2', 'dac dot{theta}')

