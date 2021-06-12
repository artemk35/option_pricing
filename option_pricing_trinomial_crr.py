# -*- coding: utf-8 -*-

#importing necessary libraries: 
import numpy as np
import math
import matplotlib.pyplot as plt

def option_pricing_trinmoial_CRR(S0, X, T, n, r, sigma, optionType, earlyExercise):

  """"
  INPUTs: 
  S0 - initial underlying price
  X - strike
  T - time to expiration in years (must be a positive number)
  n - number of periods in the binomial model (must be a positive integer)
  r -  risk free interest rate for discounitng ((must be a value greater than 0 and less than 1)
  sigma - vol parameter (must be greater than 0 and less than 1)
  optionType - specify whether it is a CALL or a PUT option (must be a string 'CALL' or 'PUT')
  earlyExercise - specify whether it is European style option or an American style option (Takes value two values. 1 - American style option and 0 - European style option)
  
  OUTPUT:
  Binomial tree of  underlying asset prices
  Binomial tree of  option values 
  """

  #calculate model parameters based on inputs: 
  dt = T/n
  pu = (np.sqrt(dt/(12*sigma**2))*(r - ((sigma**2)/2))) + 1/6
  pm = 2/3
  pd = -(np.sqrt(dt/(12*sigma**2))*(r - ((sigma**2)/2))) + 1/6
  u = np.exp(sigma*np.sqrt(3*dt))
  d = 1/u
  df = np.exp(-r*dt) # discount factor

  #Create an underlying tree holder and populate it: 
  underlying_tree = np.zeros([2*n+1, n+1])
  underlying_tree[0,0]=S0

  for idx in range(1,n+1):
    powers = np.arange(idx,-0.5,-0.5) -  np.arange(0,idx+0.5,0.5)
    underlying_tree[0:2*idx+1, idx] = S0*np.power(u,powers)

  # Create a holder for option values: 
  option_tree = np.zeros([2*n+1, n+1])

  # Calculate option's value at expiry: 
  if optionType =='CALL':
    option_tree[:, n] = np.maximum(underlying_tree[:, n] - X, 0)  
  elif optionType == 'PUT':
    option_tree[:, n] = np.maximum(X-underlying_tree[:, n], 0)

  # Populate each node of the option tree using backward induction:
  for idx in range(n,0,-1):
    option_tree[0:2*idx-1, idx-1] =  df*(pu*option_tree[0:2*idx-1,idx] + 
                                         pm*option_tree[1:2*idx, idx] + 
                                         pd*option_tree[2:idx*2+1, idx])
    if earlyExercise ==1:
      if optionType =='CALL':
        option_tree[0:2*idx-1, idx-1] = np.maximum(underlying_tree[0:2*idx-1, idx-1] - X, option_tree[0:2*idx-1, idx-1])
      elif optionType =='PUT':
        option_tree[0:2*idx-1, idx-1] = np.maximum(X - underlying_tree[0:2*idx-1, idx-1], option_tree[0:2*idx-1, idx-1])



  return underlying_tree, option_tree
