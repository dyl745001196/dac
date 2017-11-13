%(y_cur, dt, u_cur)
function y_next = sim_sys(y_cur, dt, u_cur)
    y_next = y_cur + dt*(-y_cur - sin(y_cur) + u_cur);
end