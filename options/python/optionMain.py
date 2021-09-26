import math
from datetime import date
from scipy.stats import norm


class Option:
    """
    09/18/2021 reimplement pricing of option from Matlab
    TODOLIST: need to check theta
    """
    def __init__(self, ticker, currentPrice, strikePrice, expireDate, volatility, interestRate, optionType):
        self.ticker = ticker
        self.s0 = currentPrice
        self.k = strikePrice
        self.v = volatility
        self.r = interestRate
        self.expDate = self._convert_date(expireDate)
        self.opType = optionType

    # format of dateStr: "MM/DD/YYYY"
    def _convert_date(self, dateStr):
        m, d, y = dateStr.split('/')
        return date(int(y), int(m), int(d))

    # update implied volatility
    def _update_iv(self, iv):
        self.v = iv

    # quote price
    def quotePrice(self, currDate, iv):
        cDate = self._convert_date(currDate)
        diff = self.expDate - cDate
        t = diff.days/365
        self._update_iv(iv)
        const1 = (self.r*t + self.v**2*t/2 + math.log(self.s0/self.k)) / (self.v*math.sqrt(t))
        const2 = (self.r*t - self.v**2*t/2 + math.log(self.s0/self.k)) / (self.v*math.sqrt(t))

        if self.opType == "C":
            return self.s0*norm.cdf(const1) - self.k*math.exp(-self.r*t)*norm.cdf(const2)
        else:
            return -self.s0*norm.cdf(-const1) + self.k*math.exp(-self.r*t)*norm.cdf(-const2)

    # quote Greeks
    def quoteGreeks(self, currDate, iv):
        cDate = self._convert_date(currDate)
        diff = self.expDate - cDate
        t = diff.days/365
        self._update_iv(iv)
        const1 = (self.r*t + self.v**2*t/2 + math.log(self.s0/self.k)) / (self.v*math.sqrt(t))
        const2 = (self.r*t - self.v**2*t/2 + math.log(self.s0/self.k)) / (self.v*math.sqrt(t))

        gamma = norm.cdf(const1) / (self.v*self.s0*math.sqrt(t))
        vega = 0.01*self.s0*math.sqrt(t)*(1/math.sqrt(2*math.pi)) * math.exp(-const1**2/2)
        if self.opType == "C":
            delta = norm.cdf(const1)
            theta = -self.s0*norm.cdf(const1)*self.v/(2*math.sqrt(t)) - \
                     self.r*self.k*math.exp(-self.r*t)*norm.cdf(const2)
            rho = 0.01*self.k*t*norm.cdf(const2)
        else:
            delta = norm.cdf(const1)-1
            theta = -self.s0 * norm.cdf(const1)*self.v/(2*math.sqrt(t)) + \
                     self.r * self.k * math.exp(-self.r * t) * norm.cdf(-const2)
            rho = -0.01*self.k*t*norm.cdf(-const2)
        return round(delta,4), round(gamma,4), round(theta,4), round(vega,4), round(rho,4)


# main (parameters)
ticker = "XXX"
currentPrice = 100
strikePrice = 100
expireDate = "12/17/2021"
volatility = 0.2058
interestRate = 0.01
optionType = "C"
currentDate = "10/30/2021"

op = Option(ticker=ticker, currentPrice=currentPrice, strikePrice=strikePrice, expireDate=expireDate,
            volatility=volatility, interestRate=interestRate, optionType=optionType)

# check price
price = op.quotePrice(currentDate, volatility)
print(price)

# check greeks
delta, gamma, theta, vega, rho = op.quoteGreeks(currentDate, volatility)
print(delta, gamma, theta, vega, rho)
