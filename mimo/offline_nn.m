function y = offline_nn(x)
load('weights.mat')
W0 = weight0;
b0 = weight1;
W1 = weight2;
b1 = weight3;
W2 = weight4;
b2 = weight5;
z1 = max(x*W0 + b0, 0);
z2 = max(z1*W1 + b1, 0);
y = z2*W2 + b2;
y = -y;
end