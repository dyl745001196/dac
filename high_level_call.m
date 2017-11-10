close all 

[dac_goal, dac_input] = dac_setup(1, [0:0.01:10], 1);

plot(dac_goal, 'b');
hold on 
plot(dac_input', 'r')
legend('dac\_goal to do the si', 'dac\_input to do the si');
grid on
title('input with sin(1*t)')
xlabel('time step')
ylabel('value')