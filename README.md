# option_pricing

There are 3 numerical methods commonly used to price options (can be applied to other derivatives as well):
1) Lattice methods (binomial and trinomial models)
2) Monte Carlo methods
3) Finite Difference methods

At this moment, this repository contains the following models:
1) Binomial model (allows to price European and American style options, both calls and puts)
2) Trinomial model (allows to price European and American style options, both calls and puts)
3) Finite Difference methods, including explicit, implicit, and Crank-Nicolson methods (allows to price only European options, both calls and puts). The code is written in OOP

Several useful packages for option pricing: 

[vollib](https://github.com/vollib/vollib) is a python library for calculating option prices, implied volatility and greeks.
[optlib](https://github.com/dbrojas/optlib) is a library to fetch financial option chains and price options using closed-form solutions written in Python. 
