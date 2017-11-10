% dac_setup function, freq is the freq of the input signal, t_span is the
% sim time span, y_init is the initial value of the response y
function [dac_goal, dac_input] = dac_setup(freq, t_span, y_init)

u = sin(freq*t_span);
% the initial value of y
[t, y] = ode45(@(t, y) - y - sin(y) + sin(freq*t), t_span, y_init);
% calc the grad from the diff methods as is x(k+1) - x(k)
dy = diff(y);
dt = diff(t); 
%calc the grad
grad = dy ./ dt;
% establish the true grad
grad_true = -y -sin(y); 
%shift one step to align
grad_true = grad_true(2:end); 
y = y(2:end)
% gather the data to do the si 

dac_goal = grad - u(2:end)';
dac_input = u(2:end)';


