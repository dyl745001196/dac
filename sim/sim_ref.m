%(y_cur, dt, u_cur)
function y_next = sim_ref(y_cur, dt, u_cur)
    T_const = 20;
    y_next(1) = y_cur(1) + dt*(-T_const* y_cur(1)  + T_const*u_cur(1));
    y_next(2) = y_cur(2) + dt*(-T_const* y_cur(2)  + T_const*u_cur(2));
end