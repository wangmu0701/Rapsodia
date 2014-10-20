! This file was generated by Rapsodia (see www.mcs.anl.gov/Rapsodia)
module RAabs
  use RAprec
  use RAtypes
  implicit none
  interface abs
    module procedure absRArealS
    module procedure absRArealD
  end interface abs
contains 
  elemental function absRArealS(a) result(r)
    type(RArealS),intent(in)::a
    type(RArealS)::r
    real(kind=RAsKind)::factor_0
    real(kind=RAsKind)::factor_d
    include 'RAabs.i90'
  end function absRArealS
  elemental function absRArealD(a) result(r)
    type(RArealD),intent(in)::a
    type(RArealD)::r
    real(kind=RAdKind)::factor_0
    real(kind=RAdKind)::factor_d
    include 'RAabs.i90'
  end function absRArealD
end module RAabs