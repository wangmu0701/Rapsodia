! This file was generated by Rapsodia (see www.mcs.anl.gov/Rapsodia)
module RAsqrt
  use RAprec
  use RAtypes
  implicit none
  interface sqrt
    module procedure sqrtRArealS
    module procedure sqrtRArealD
    module procedure sqrtRAcomplexS
    module procedure sqrtRAcomplexD
  end interface sqrt
contains 
  elemental function sqrtRArealS(a) result(r)
    type(RArealS),intent(in)::a
    type(RArealS)::r
    real(kind=RAsKind)::recip
    include 'RAsqrt.i90'
  end function sqrtRArealS
  elemental function sqrtRArealD(a) result(r)
    type(RArealD),intent(in)::a
    type(RArealD)::r
    real(kind=RAdKind)::recip
    include 'RAsqrt.i90'
  end function sqrtRArealD
  elemental function sqrtRAcomplexS(a) result(r)
    type(RAcomplexS),intent(in)::a
    type(RAcomplexS)::r
    complex(kind=RAsKind)::recip
    include 'RAsqrtZ.i90'
  end function sqrtRAcomplexS
  elemental function sqrtRAcomplexD(a) result(r)
    type(RAcomplexD),intent(in)::a
    type(RAcomplexD)::r
    complex(kind=RAdKind)::recip
    include 'RAsqrtZ.i90'
  end function sqrtRAcomplexD
end module RAsqrt