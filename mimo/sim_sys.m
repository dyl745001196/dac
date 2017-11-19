%(y_cur, dt, u_cur)
function y_next = sim_sys(y_cur, dt, u_cur)
    y_next(1) = y_cur(1) + dt*(-y_cur(1) - y_cur(2) - sin(y_cur(1))                 + u_cur(1));
    y_next(2) = y_cur(2) + dt*(-y_cur(1) + y_cur(2) - sin(y_cur(1)) + sin(y_cur(2)) + u_cur(2));
end