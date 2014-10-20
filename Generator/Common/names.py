##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
## fixed names
#
# names used by the generator;
# in case naming conflicts with code using Rapsodia these should be changed
class Fixed:
  ## @var pN
  # tool specific prefix name
  pN = 'RA'
  rN = 'RAR'
#R surfix means reverse
#RR means Rapsodia Reserse

  ## @var vN
  # name of value portion
  vN = 'v'

  ## @var aN
  # name of adjoint portion, or the address can be used as marker
  aN = 'a'

  lN = 'loc'

  ## @var sN
  # name of slice portion
  sN = 's'

  ## @var precDeclN
  # name of the reference to precision declarations
  precDeclN=pN+'prec'

  ## @var precDeclN
  # name of the reference to type declarations
  typeDeclN=pN+'types'

## variable  names
#  
# the names of the active type elements generated
# for a given order and direction count
class Variable:

  ## @var dN
  # names of derivative portions list of lists of names first per direction, 
  # then each name per order
  dN = None

## names of derivative portions list of lists of names first per direction, then each name per order
# @param d number of directions
# @param o maximal order
def init(d , o):
  import Common.parameters as cp
  if cp.slices == 0:
    dirRange = d
  else:
    dirRange = d / cp.slices

  Variable.dN=[ ['d%i_%i' % (dir,ord)
                 for ord in range(1,o+1,1) ]
                 for dir in range(1,dirRange+1,1) ]
