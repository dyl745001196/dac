%(y_cur, dt, u_cur)
function y_next = sim_ref(y_cur, dt, u_cur)
    y_next = y_cur + dt*(-5* y_cur  + 5*u_cur);
end