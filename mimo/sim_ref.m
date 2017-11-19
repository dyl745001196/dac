%(y_cur, dt, u_cur)
function y_next = sim_ref(y_cur, dt, u_cur)
    y_next(1) = y_cur(1) + dt*(-5* y_cur(1)  + 5*u_cur(1));
    y_next(2) = y_cur(2) + dt*(-5* y_cur(2)  + 5*u_cur(2));
end