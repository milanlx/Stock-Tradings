% simulate Brownian Motion

%% part I: continuous 
%% B(n+1) = B(n) + X_i

t = 1;
n = 10000;
B = zeros(n,1);     % B(0) = 0
for i=2:1:n
    % generate normal variable N(0, t/n)
    x = normrnd(0, sqrt(t/n));
    B(i) = B(i-1) + x;
end
x_axis = linspace(0,t,n*t);
plot(x_axis, B)


%% part II: from random walk
%% S_t^n = S_nt/sqrt(n)

n = 100;
t = 100;
randWalk = zeros(n*t,1);
for i=2:1:n*t
    % generate Bernoulli variable (p=0.5)
    x = binornd(1,0.5);
    res = 2*x - 1;      % map of (0 -> -1, 1 -> 1) 
    randWalk(i) = randWalk(i-1) + res;
end
% scaled the random walk to Brownian motion
B_rand = randWalk/sqrt(n);

% plotting 
x_axis = linspace(0,t,n*t);
%plot(x_axis, B_rand)
