!#########################################################
! This file is part of Rapsodia released under the LGPL. #
! The full COPYRIGHT notice can be found in the top      #
! level directory of the Rapsodia distribution           #
!#########################################################
subroutine head(x,y)
  include 'RAinclude.i90'
  type(RArealD) x(3),y
  y=sin(x(1))*sin(x(2))*sin(x(3))
end
