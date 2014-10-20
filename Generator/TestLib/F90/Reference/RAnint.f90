! This file was generated by Rapsodia (see www.mcs.anl.gov/Rapsodia)
module RAnint
  use RAprec
  use RAtypes
  implicit none
  interface nint
    module procedure nintRArealS
    module procedure nintRArealD
  end interface nint
contains 
  elemental function nintRArealS(a) result(r)
    type(RArealS),intent(in)::a
    integer::r
    include 'RAnint.i90'
  end function nintRArealS
  elemental function nintRArealD(a) result(r)
    type(RArealD),intent(in)::a
    integer::r
    include 'RAnint.i90'
  end function nintRArealD
end module RAnint