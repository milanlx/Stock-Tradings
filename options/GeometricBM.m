%% simulate Geometric Brownian Motion, 
%% Example 8.15

% parameters 
G_0 = 80;               % initial price
t = 90;                 % number of days
mu = 0.10;              % drift
sigma = 0.50;           % volatility
N = 50;                % number of trail

% parameter for Brownian Motion
t_B = 1;                % duration of t (in year)
n = 365;                % number of data point (in day)

% coutour of E(G_t) +/- 2 std(G_t)
coutour_pos = zeros(t,1);
coutour_neg = zeros(t,1);

for i=0:1:t-1
    i_year = i/365;
    E_Gt = G_0 * exp(i_year*(mu+sigma^2/2));
    Var_Gt = G_0 ^2 * exp(2*i_year*(mu+sigma^2/2)) * (exp(i_year*sigma^2)-1);
    coutour_pos(i+1) = E_Gt + 2*sqrt(Var_Gt);
    coutour_neg(i+1) = E_Gt - 2*sqrt(Var_Gt);
end



% plot 
x_axis = linspace(0,t,t);
plot(x_axis, coutour_pos, '--r', 'LineWidth',2);
hold on
plot(x_axis, coutour_neg, '--r', 'LineWidth',2);
hold on 
plot(x_axis, G_0*ones(t,1), '--r', 'LineWidth',2);
hold on 
% plot N trial of simulation
for j = 1:1:N
    % simulate standard Brownian Motion
    B = zeros(365,1);     % B(0) = 0
    for i=2:1:n
        x = normrnd(0, sqrt(t_B/n));
        B(i) = B(i-1) + x;
    end
    
    % simulate geometric Brownian Motion
    Gt = zeros(t,1);
    for i=1:1:t
        i_year = i/365;
        Gt(i) = G_0 * exp(mu*i_year + sigma*B(i));
    end
    
    % plot
    plot(x_axis, Gt, 'LineWidth', 0.5, 'Color',[.7 .7 .7])
    %hold on
end

