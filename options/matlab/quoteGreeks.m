%% quote the greeks of call or put options  
%% Generate the greek of (call) option based on the solutio to 
%  Black-Scholes euqation, assuming there is no dividend
%% Parameters
% S0                                % initial price
% T                                 % time till expiration (in years)
% r                                 % interest rate (continuous compound)
% K                                 % strike price 
% v                                 % volatility (in year)
% type                              % "C" or "P"

function [delta, gamma, theta, vega, rho] = quoteGreeks(S0, T, r, K, v, type)
    % compute N1 and N2
    const1 = (r*T + v^2*T/2 + log(S0/K)) / (v*sqrt(T));
    const2 = (r*T - v^2*T/2 + log(S0/K)) / (v*sqrt(T));
    
    % delta 
    if type == "C"
        delta = normcdf(const1);
    else
        delta = normcdf(const1)-1;
    end
    
    % gamma 
    gamma = normpdf(const1)/(v*S0*sqrt(T));
    
    % theta
    if type == "C"
        theta = -S0*normpdf(const1)*v/(2*sqrt(T)) - r*K*exp(-r*T)*normcdf(const2);
    
    else
        theta = -S0*normcdf(const1)*v/(2*sqrt(T)) + r*K*exp(-r*T)*normcdf(-const2);
    end
    
    % vega
    vega = 0.01 * S0 * sqrt(T) * (1/sqrt(2*pi)) * exp(-const1^2/2);
    
    % rho
    if type == "C"
        rho = 0.01 * K * T * normcdf(const2);
    else
        rho = -0.01 * K * T * normcdf(-const2);
    end
    
end
