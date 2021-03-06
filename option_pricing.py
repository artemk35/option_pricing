
# Import libraries required for the code: 
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import math

"""This python notebook aims at pricing options (call and put) using binomial tree applying Cox, Ross, and Rubinstein model. The function can price either American or European style option.

# Classical binomial Cox, Ross and Rubinstein
"""

def binomial_option_CRR(S0, X, T, n, r, sigma, optionType, earlyExercise):
  """
  # INPUTS: 
  S0 - initial stock px (must be a positive numeric value)
  X - strike price of an option (must be a positive numeric value)
  T - time to expiration in years (must be a positive number)
  n - number of periods in the binomial model (must be a positive integer)
  r - risk free interest rate for discounitng ((must be a value greater than 0 and less than 1)
  sigma - vol parameter (must be greater than 0 and less than 1)
  optionType - specify whether it is a CALL or a PUT option (must be a string 'CALL' or 'PUT')
  earlyExercise - specify whether it is European style option or an American style option (Takes value two values. 1 - American style option and 0 - European style option)
  
  #OUTPUT:
  Binomial tree of an underlying asset
  Binomial tree of an option
  matrix of deltas
  matrix of gammas
  """
  

  # Calculate CRR model parameters: 
  dt = T/n
  a = math.exp(r*dt)
  u = math.exp(sigma*math.sqrt(dt))
  d = 1/u
  p = (a - d)/(u - d)

  # Create a matrix to hold the binomial tree: 
  underlying_price_holder = np.zeros([n+1, n+1])
  # populate binomial tree with underlying asset prices:
  for idx in range(n+1):
    for jdx in range(n+1):
      underlying_price_holder[jdx,idx] = S0*(d**jdx)*(u**(idx-jdx))
  
  # Create a matrix to hold the option values
  option_value_tree = np.zeros([n+1, n+1])
  # Populate the tree with backward induction: 
  if optionType == 'CALL':
    option_value_tree[:,n] = np.maximum((underlying_price_holder[:,n]-X), np.zeros(n+1))
  elif optionType=='PUT': 
    option_value_tree[:,n] = np.maximum((X - underlying_price_holder[:,n]), np.zeros(n+1))

  for idx in range(n,0,-1):
    option_value_tree[0:idx, idx-1] = np.exp(-r*dt)*(p*option_value_tree[0:idx, idx] + (1-p)*option_value_tree[1:idx+1, idx])
    if earlyExercise==1:
      if optionType =='CALL':
        option_value_tree[0:idx, idx-1] = np.maximum(underlying_price_holder[0:idx, idx-1]-X, option_value_tree[0:idx, idx-1])
      elif optionType =='PUT':
        option_value_tree[0:idx, idx-1] = np.maximum(X - underlying_price_holder[0:idx, idx-1], option_value_tree[0:idx, idx-1])

  # Calculate the sensitivities: 
  dS = np.diff(underlying_price_holder)
  delta_tree = np.diff(option_value_tree)/dS
  gamma_tree=np.diff(delta_tree)/dS[:,1:]


  return underlying_price_holder, option_value_tree, delta_tree, gamma_tree

[stock, option, delta,gamma ]=binomial_option_CRR(100, 100, 1, 3, 0.01, 0.2, 'CALL', 0)

