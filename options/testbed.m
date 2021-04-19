%% 12/02/2020 test projection profit of current holdings


% TWTR
indexTicker = "TWTR";
S0 = 47.18;                    
T  = 28/365;                
r  = 0.01;                  
K  = 50;                     
v  = 0.4051;                  
type = "C";

price = quotePrice(S0, T, r, K, v, type);
%fprintf("test: the price for %s at %d is: %.1f\r", indexTicker, K, price*100);

% projection: get 50 before 12/11
price = quotePrice(52, 21/365, r, K, v, type);
%fprintf("  -- reach 52 before 12/11, the price is: %.1f\r", price*100);


% PING
indexTicker = "PING";
S0 = 22.34;                    
T  = 80/365;                
r  = 0.01;                  
K  = 30;                     
v  = 0.6334;                  
type = "C";

price = quotePrice(S0, T, r, K, v, type);
%fprintf("test: the price for %s at %d is: %.1f\r", indexTicker, K, price*100);

% projection: get 30 before 12/31
price = quotePrice(30, 50/365, r, K, v, type);
%fprintf("  -- reach 30 before 12/31, the price is: %.1f\r", price*100);


%% 12/16/2020 test projection profits 

% VALE
indexTicker = "IQ";
S0 = 15.29;                    
T  = 250/365;                
r  = 0.01;                  
K  = 20;                     
v  = 0.69;                  
type = "C";
St = 20;            % prejected price 

price = quotePrice(S0, T, r, K, v, type);
fprintf("test: the price for %s at %d is: %.1f\r", indexTicker, K, price*100);

% projection: get St before 05/15
price = quotePrice(St, 220/365, r, K, v, type);
fprintf("  -- reach %.1f before 01/31, the price is: %.1f\r", St, price*100);


