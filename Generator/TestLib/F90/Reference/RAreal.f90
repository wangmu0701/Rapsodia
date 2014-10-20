! This file was generated by Rapsodia (see www.mcs.anl.gov/Rapsodia)
module RAreal
  use RAprec
  use RAtypes
  implicit none
  interface real
    module procedure realRAcomplexS
    module procedure realRAcomplexD
  end interface real
contains 
  elemental function realRAcomplexS(a) result(r)
    type(RAcomplexS),intent(in)::a
    type(RArealS)::r
    include 'RAreal.i90'
  end function realRAcomplexS
  elemental function realRAcomplexD(a) result(r)
    type(RAcomplexD),intent(in)::a
    type(RArealD)::r
    include 'RAreal.i90'
  end function realRAcomplexD
end module RAreal
