dt = 0.01;

x_cur = [0 0];
x_m_cur = [0 0];

theta_hat = [1 0;
             0 1];
theta = theta_hat;

k_x_hat = [-5 0;
            0 -5];
k_r_hat = [5 0;
           0 5];
 

gamma_x = [0.1 0;
           0 1];
gamma_r = gamma_x;

P = [1 0;
     0 1];

x_set = [x_cur];
x_m_set = [x_m_cur];

for i = 1:4000
    r = [0.8*sin(i / 100) -0.7*sin(i/100)];
    %r = [1 1];
    DL_x_r = offline_nn(x_cur)* theta_hat + k_x_hat * x_cur' + k_r_hat * r';
    x_next = sim_sys(x_cur, dt, DL_x_r);
    x_m_next = sim_ref(x_m_cur, dt, r);
    x_cur = x_next;
    x_m_cur = x_m_next;
    x_set = [x_set; x_cur];
    x_m_set = [x_m_set; x_m_cur];
    
    e = x_cur - x_m_cur;
    
    theta_hat = theta_hat -dt*gamma_x*x_cur'*e*P;
    k_x_hat = k_x_hat -dt*gamma_r*r'*e*P;
    k_r_hat = k_r_hat -dt*offline_nn(x_cur)'*e*P;

end
subplot(2, 1, 1)
cla
plot(x_m_set(:, 1), '--r', 'LineWidth', 2)
hold on 
plot(x_set(:, 1), 'b', 'LineWidth', 2)
legend('ref system state y1', 'dac')
subplot(2, 1, 2)
cla
plot(x_m_set(:, 2), '--r', 'LineWidth', 2)
hold on 
plot(x_set(:, 2), 'b', 'LineWidth', 2)
legend('ref system state y2', 'dac')