steps = 1:15;
steps = steps';
% the highest item
N = 4;
coeff = polyfit(steps, scale_dot_theta, N);

pred = polyval(coeff, steps);

plot(scale_dot_theta)
hold on
plot(pred)