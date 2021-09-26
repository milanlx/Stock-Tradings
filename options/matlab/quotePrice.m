%% quote the call or put price 
%% Generate the curve of (call) option based on the solutio to 
%  Black-Scholes euqation, assuming there is no dividend
%% Parameters
% S0                                % initial price
% T                                 % time till expiration (in years)
% r                                 % interest rate (continuous compound)
% K                                 % strike price 
% v                                 % volatility (in year)
% type                              % "C" or "P"

function price = quotePrice(S0, T, r, K, v, type)
    % compute N1 and N2
    const1 = (r*T + v^2*T/2 + log(S0/K)) / (v*sqrt(T));
    const2 = (r*T - v^2*T/2 + log(S0/K)) / (v*sqrt(T));
    
    % call 
    if type == "C"
        price = S0*normcdf(const1) - K*exp(-r*T)*normcdf(const2);
    else
        price = -S0*normcdf(-const1) + K*exp(-r*T)*normcdf(-const2);
    end
end
