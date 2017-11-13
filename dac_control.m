dt = 0.01;

k_x_hat = -5;
k_r_hat = 5;
theta_hat = 1;
theta = 1;

x_cur = 0;
x_m_cur = 0;

gamma_x = 50;
gamma_r = gamma_x;

x_set = [x_cur];
x_m_set = [x_m_cur];

% discrete sim of sys
for i = 1:1000
    r = sin(i/100);
    DL_x_r = offline_nn(x_cur)* theta_hat + k_x_hat * x_cur + k_r_hat * r;
    x_next = sim_sys(x_cur, dt, DL_x_r);
    x_m_next = sim_ref(x_m_cur, dt, r);
    x_cur = x_next;
    x_m_cur = x_m_next;
    x_set = [x_set x_cur];
    x_m_set = [x_m_set x_m_cur];
    
    e = x_cur - x_m_cur;
    
    theta_hat = -e * dt * offline_nn(x_cur) + theta_hat;
    k_x_hat = - gamma_x * e * x_cur;
    k_r_hat = - gamma_r * e * r;

end

plot(x_m_set, '--r', 'LineWidth', 2)
hold on 
plot(x_set, 'b', 'LineWidth', 2)
legend('ref system', 'dac')