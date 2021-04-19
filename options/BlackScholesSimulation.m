%% Generate the curve of (call) option bssed on the solutio to 
%  Black-Scholes euqation, assuming there is no dividend

% PARAMETERS 
S0 = 25;                    % initial price
T  = 38/365;                % time till expiration (in years)
r  = 0.01;                  % interest rate (continuous compound)
K  = 30;                    % strike price 
v  = 0.66;                  % volatility (in year)
type = "C";                 % call or put


price = quotePrice(S0, T, r, K, v, type);
price_quarter = quotePrice(S0, T/4, r, K, v, type);

% given a price trajectory, simulate the option price till expiration
t = T*365;
stock_price = zeros(t,1);
stock_price(1) = S0;
stock_price(2:8) = 27;
stock_price(9:15) = 30;
stock_price(16:end) = 31;
option_price = zeros(t,1);

for i=1:1:t
    temp_T = T - i*1/365;
    temp_S0 = stock_price(i);
    option_price(i) = quotePrice(temp_S0, temp_T, r, K, v, type);
end

% plot 
x_axis = linspace(0,t,t);

subplot(2,1,1); plot(x_axis, stock_price, '*k', 'LineWidth',2)
subplot(2,1,2); plot(x_axis, option_price*100, '--r', 'LineWidth',2)