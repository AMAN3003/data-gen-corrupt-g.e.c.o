# Functions that can generate attribute values.
#
# These are functions that can be used in the GenerateFuncAttribute() class
# (see module generator.py). They generate values according to some internal
# functionality.
#
# The requirement of any such functions are:
# 1) that it must return a string
# 2) it can have been 0 and 5 parameters
# 
#
# Examples of such functions are:
# - Australian telephone numbers
# - Japanese telephone numbers
# - Credit card numbers
# - US social security numbers
# - Japanese social security numbers
# - Uniformly distributed age values between 0 and 100
# - Normally distributed age values between 0 and 110
# etc.

# Peter Christen and Dinusha Vatsalan, January-March 2012
# =============================================================================
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# =============================================================================

import random
from random import Random #for the real credit card 
gene = Random()
gene.seed()
import copy
import basefunctions

from bisect import bisect
import math
# =============================================================================
# for the generating the age based on the australian population pyramid
def Prob_Weighted_Choice(prob_choices):
    values=()
    Weights_Percentage=()
    values, Weights_Percentage = zip(*prob_choices)
    total = 0
    Cum_Weights_Percentage = []
    for w in Weights_Percentage:
        total += w
        Cum_Weights_Percentage.append(total)
    x = random.random() * total
    i = bisect(Cum_Weights_Percentage, x)
    return values[i]
# =============================================================================
# real credit card starting prefix
Prefix_JCB_List = [['3', '5']]

Prefix_MasterCard_List = [
        ['5', '1'], ['5', '2'], ['5', '3'], ['5', '4'], ['5', '5']] #major

Prefix_Visa_List = [
        ['4', '5', '3', '9'],
        ['4', '5', '5', '6'],
        ['4', '9', '1', '6'],
        ['4', '5', '3', '2'],
        ['4', '9', '2', '9'],
        ['4', '0', '2', '4', '0', '0', '7', '1'],
        ['4', '4', '8', '6'],
        ['4', '7', '1', '6'],
        ['4']]        #major

Prefix_Discover_List = [['6', '0', '1', '1']]

# =============================================================================

# -----------------------------------------------------------------------------
#
def generate_phone_number_australia():
  """Randomly generate an Australian telephone number made of a two-digit area
     code and an eight-digit number made of two blocks of four digits (with a
     space between). For example: `02 1234 5678'

     For details see: http://en.wikipedia.org/wiki/ \
                      Telephone_numbers_in_Australia#Personal_numbers_.2805.29
  """
  
  area_code = random.choice(['02', '03', '04', '07', '08'])

  number1 = random.randint(1,9999)
  number2 = random.randint(1,9999)

  oz_phone_str = str(area_code)+' '+str(number1).zfill(4)+' '+ \
                 str(number2).zfill(4)
  assert len(oz_phone_str) == 12
  assert oz_phone_str[0] == '0'

  return oz_phone_str

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
#
def Credit_Card_Complete(prefix, length):
    """
    'prefix' IS THE START OF CREDIT CARD WHICH IS DIFFERENT FOR DIFFERENT TYPES OF CREDIT AND IS STRING 
    'length' OF THE CREDIT CARD NO IS 16 DIGIT
    """
    Credit_Card_Number = prefix

    # generate credit card digits

    while len(Credit_Card_Number) < (length - 1):
        d = str(gene.choice(range(0, 10)))
        Credit_Card_Number.append(d)

    # Calculate SumCC of the credit card 
    IterPos = 0
    SumCC = 0
    reversedCredit_Card_Number = []
    reversedCredit_Card_Number.extend(Credit_Card_Number)
    reversedCredit_Card_Number.reverse()
    #LUH'S FORMULA 
    while IterPos < length - 1:

        OddDIG = int(reversedCredit_Card_Number[IterPos]) * 2
        if OddDIG > 9:
            OddDIG -= 9

        SumCC += OddDIG

        if IterPos != (length - 2):

            SumCC += int(reversedCredit_Card_Number[IterPos + 1])

        IterPos += 2

    # Calculate check digit

    Ccdigit_Check = ((SumCC / 10 + 1) * 10 - SumCC) % 10

    Credit_Card_Number.append(str(Ccdigit_Check))

    return ''.join(Credit_Card_Number)

def C_C_Number(RanD, Prefix_Lists, length, maxNoEachC_C):

    C_C_lists = []

    while len(C_C_lists) < maxNoEachC_C:

        Credit_Card_Number = copy.copy(RanD.choice(Prefix_Lists))
        C_C_lists.append(Credit_Card_Complete(Credit_Card_Number, length))

    return C_C_lists

def generate_credit_card_number():
  """Generate a credit card that pass the MOD 10 check (Luhn formula).
     REAL CREDIT CARD NO used in e-commerce Websites. For example: '1234 5678 9012 3456'

     For details see: http://en.wikipedia.org/wiki/Bank_card_number
  """
  
  mastercard = C_C_Number(gene, Prefix_MasterCard_List, 16, 7)
  visa16 = C_C_Number(gene, Prefix_Visa_List, 16, 9)
  
  
  # Minor cards
  discover = C_C_Number(gene, Prefix_Discover_List, 16, 2)
  jcb = C_C_Number(gene, Prefix_JCB_List, 16, 2)
  C_C_lists=[]
  C_C_lists=mastercard+visa16+discover+jcb
  real_credit_card_number=random.choice(C_C_lists)
  creditcardparts=list(map(''.join, zip(*[iter(real_credit_card_number)]*4)))


  number1 = creditcardparts[0]
  assert number1 > 0

  number2 = creditcardparts[1]
  assert number2 > 0

  number3 = creditcardparts[2]
  assert number3 > 0

  number4 = creditcardparts[3]
  assert number4 > 0

  cc_str = str(number1).zfill(4)+' '+str(number2).zfill(4)+' '+ \
           str(number3).zfill(4)+' '+str(number4).zfill(4)

  assert len(cc_str) == 19

  return cc_str

# -----------------------------------------------------------------------------
#
def generate_uniform_value(min_val, max_val, val_type):
  """Randomly generate a numerical value according to a uniform distribution
     between the minimum and maximum values given.

     The value type can be set as 'int', so a string formatted as an integer
     value is returned; or as 'float1' to 'float9', in which case a string
     formatted as floating-point value with the specified number of digits
     behind the comma is returned.

     Note that for certain situations and string formats a value outside the
     set range might be returned. For example, if min_val=100.25 and
     val_type='float1' the rounding can result in a string value '100.2' to
     be returned.

     Suitable minimum and maximum values need to be selected to prevent such a
     situation.
  """

  basefunctions.check_is_number('min_val', min_val)
  basefunctions.check_is_number('max_val', max_val)
  assert min_val < max_val

  r = random.uniform(min_val, max_val)

  return basefunctions.float_to_str(r, val_type)

# -----------------------------------------------------------------------------
#


def generate_population_pyramid_age(min_val_pyramidal, max_val_pyramidal):
  """Randomly generate an age value (returned as integer) according to a
     population pyramidal distribution of australian people 
     between the minimum and maximum values given.
     
     This function is simple a shorthand for:

       generate_popul_pyramid_value(min_val_pyramidal, max_val_pyramidal, 'int')
  """
  
  assert min_val_pyramidal >= 0
  assert max_val_pyramidal <= 130

  return generate_popul_pyramid_value(min_val_pyramidal, max_val_pyramidal, 'int')

def generate_popul_pyramid_value(min_val_pyramidal, max_val_pyramidal, val_type):
  """Randomly generate an age value (returned as integer) according to a
     population pyramidal distribution of australian people 
     between the minimum and maximum values given.
     For details see:
     https://populationpyramid.net/australia/2015/
  """

  basefunctions.check_is_number('min_val', min_val_pyramidal)
  basefunctions.check_is_number('max_val', max_val_pyramidal)
  assert min_val_pyramidal < max_val_pyramidal

  population_pyramid_data=[]
  population_pyramid_data+=[([0,4],6.4),([5,9],6.4),([10,14],5.9),([15,19],6.2),([15,19],6.2),([20,24],7), 
        ([25,29],7.5),([30,34],7.4),([35,39],6.4),([35,39],6.4),([40,44],7.1),([45,49],6.4),([50,54],6.8),
        ([55,59],6.1),([60,64],5.3),([65,69],5.0),([70,74],3.5),([70,74],3.5),([75,79],2.7),([80,84],2),
        ([85,89],1.3),([90,94],0.6),([95,99],0.1)]
  age_gen=Prob_Weighted_Choice(population_pyramid_data)
    
  min_val_age_interval=age_gen[0]
  max_val_age_interval=age_gen[1]
  r=random.uniform(min_val_age_interval, max_val_age_interval)
  #r = random.uniform(min_val, max_val)

  return basefunctions.float_to_str(r, val_type)

# -----------------------------------------------------------------------------
#

def generate_uniform_age(min_val, max_val):
  """Randomly generate an age value (returned as integer) according to a
     uniform distribution between the minimum and maximum values given.

     This function is simple a shorthand for:

       generate_uniform_value(min_val, max_val, 'int')
  """

  assert min_val >= 0
  assert max_val <= 130

  return generate_uniform_value(min_val, max_val, 'int')

# -----------------------------------------------------------------------------

def generate_normal_value(mu, sigma, min_val, max_val, val_type):
  """Randomly generate a numerical value according to a normal distribution
     with the mean (mu) and standard deviation (sigma) given.

     A minimum and maximum allowed value can given as additional parameters,
     if set to None then no minimum and/or maximum limit is set.

     The value type can be set as 'int', so a string formatted as an integer
     value is returned; or as 'float1' to 'float9', in which case a string
     formatted as floating-point value with the specified number of digits
     behind the comma is returned.
  """

  basefunctions.check_is_number('mu', mu)
  basefunctions.check_is_number('sigma', sigma)
  assert sigma > 0.0

  if (min_val != None):
    basefunctions.check_is_number('min_val', min_val)
    assert min_val <= mu

  if (max_val != None):
    basefunctions.check_is_number('max_val', max_val)
    assert max_val >= mu

  if ((min_val != None) and (max_val != None)):
    assert min_val < max_val

  if (min_val != None) or (max_val != None):
    in_range = False  # For testing if the random value is with the range
  else:
    in_range = True

  r = random.normalvariate(mu, sigma)

  while (in_range == False):
    if ((min_val == None) or ((min_val != None) and (r >= min_val))):
      in_range = True

    if ((max_val != None) and (r > max_val)):
      in_range = False

    if (in_range == True):
      r_str = basefunctions.float_to_str(r, val_type)
      r_test = float(r_str)
      if (min_val != None) and (r_test < min_val):
        in_range = False
      if (max_val != None) and (r_test > max_val):
        in_range = False

    if (in_range == False):
      r = random.normalvariate(mu, sigma)

  if (min_val != None):
    assert r >= min_val
  if (max_val != None):
    assert r <= max_val

  return basefunctions.float_to_str(r, val_type)

# -----------------------------------------------------------------------------
#
def generate_normal_age(mu, sigma, min_val, max_val):
  """Randomly generate an age value (returned as integer) according to a
     normal distribution following the mean and standard deviation values
     given, and limited to age values between (including) the minimum and
     maximum values given.

     This function is simple a shorthand for:

       generate_normal_value(mu, sigma, min_val, max_val, 'int')
  """

  assert min_val >= 0
  assert max_val <= 130

  age = generate_normal_value(mu, sigma, min_val, max_val, 'int')

  while ((int(age) < min_val) or (int(age) > max_val)):
    age = generate_normal_value(mu, sigma, min_val, max_val, 'int')

  return age

# =============================================================================

# If called from command line perform some examples: Generate values
#
if (__name__ == '__main__'):

  num_test = 20

  print 'Generate %d Australian telephone numbers:' % (num_test)
  for i in range(num_test):
    print ' ', generate_phone_number_australia()
  print

  print 'Generate %d credit card numbers:' % (num_test)
  for i in range(num_test):
    print ' ', generate_credit_card_number()
  print

  print 'Generate %d uniformly distributed integer numbers between -100' % \
        (num_test) + ' and -5:'
  for i in range(num_test):
    print ' ', generate_uniform_value(-100, -5, 'int'),
  print

  print 'Generate %d uniformly distributed floating-point numbers with ' % \
        (num_test) + '3 digits between -55 and 55:'
  for i in range(num_test):
    print ' ', generate_uniform_value(-55, 55, 'float3')
  print

  print 'Generate %d uniformly distributed floating-point numbers with ' % \
        (num_test) + '7 digits between 147 and 9843:'
  for i in range(num_test):
    print ' ', generate_uniform_value(147, 9843, 'float7')
  print

  print 'Generate %d uniformly distributed age values between 0 and 120:' % \
        (num_test)
  for i in range(num_test):
    print ' ', generate_uniform_age(0, 120)
  print

  print 'Generate %d uniformly distributed age values between 18 and 65:' % \
        (num_test)
  for i in range(num_test):
    print ' ', generate_uniform_age(18, 65)
  print

  print 'Generate %d normally distributed integer numbers between -200' % \
        (num_test) + ' and -3 with mean -50 and standard deviation 44:'
  for i in range(num_test):
    print ' ', generate_normal_value(-50, 44, -200, -3, 'int')
  print

  print 'Generate %d normally distributed floating-point numbers with ' % \
        (num_test) + '5 digits between -100 and 100 and with mean 22 and ' + \
        'standard deviation 74:'
  for i in range(num_test):
    print ' ', generate_normal_value(22, 74, -100, 100, 'float5')
  print

  print 'Generate %d normally distributed floating-point numbers with ' % \
        (num_test) + '9 digits with mean 22 and standard deviation 74:'
  for i in range(num_test):
    print ' ', generate_normal_value(22, 74, min_val=None, max_val= None,
                                     val_type='float9')
  print

  print 'Generate %d normally distributed floating-point numbers with ' % \
        (num_test) + '2 digits with mean 22 and standard deviation 24 that' + \
        ' are larger than 10:'
  for i in range(num_test):
    print ' ', generate_normal_value(22, 74, min_val=10, max_val=None,
                                     val_type='float2')
  print

  print 'Generate %d normally distributed floating-point numbers with ' % \
        (num_test) + '4 digits with mean 22 and standard deviation 24 that' + \
        ' are smaller than 30:'
  for i in range(num_test):
    print ' ', generate_normal_value(22, 74, min_val=None, max_val=40,
                                     val_type='float4')
  print

  print 'Generate %d normally distributed age values between 0 and 120' % \
        (num_test) + ' with mean 45 and standard deviation 22:'
  for i in range(num_test):
    print ' ', generate_normal_age(45, 22, 0, 120)
  print

  print 'Generate %d normally distributed age values between 18 and 65' % \
        (num_test) + ' with mean 30 and standard deviation 10:'
  for i in range(num_test):
    print ' ', generate_normal_age(30, 10, 18, 65)
  print
