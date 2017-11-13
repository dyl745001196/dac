y_cur = 0;
y_set =[y_cur];
for i = 1:1000
    y_next = sim_sys(y_cur, 0.01, sin(i/100));
    y_cur = y_next;
    y_set = [y_set y_cur];
end
i = 1:1000;
ref = sin(i/100);
plot(ref, '--r', 'LineWidth', 2)
hold on 
plot(y_set, 'b', 'LineWidth', 2)
legend('ref system', 'no controller')