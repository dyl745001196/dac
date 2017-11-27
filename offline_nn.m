function y = offline_nn(x)
load('weights.mat')
W0 = weight0;
b0 = weight1;
W1 = weight2;
b1 = weight3;
y = max(W0*x +b0, 0)*W1 + b1 ;
y = -y;
end