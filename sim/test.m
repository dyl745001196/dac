x_m_cur = [0 0];
for i = 1:1000
    r = [1 0]
    x_m_next = sim_ref(x_m_cur, dt, r);
    