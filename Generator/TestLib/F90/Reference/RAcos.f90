! This file was generated by Rapsodia (see www.mcs.anl.gov/Rapsodia)
module RAcos
  use RAprec
  use RAtypes
  implicit none
  interface cos
    module procedure cosRArealS
    module procedure cosRArealD
    module procedure cosRAcomplexS
    module procedure cosRAcomplexD
  end interface cos
contains 
  elemental function cosRArealS(a) result(c)
    type(RArealS),intent(in)::a
    type(RArealS)::c
    type(RArealS)::s
    type(RArealS)::t
    include 'RAsincos.i90'
  end function cosRArealS
  elemental function cosRArealD(a) result(c)
    type(RArealD),intent(in)::a
    type(RArealD)::c
    type(RArealD)::s
    type(RArealD)::t
    include 'RAsincos.i90'
  end function cosRArealD
  elemental function cosRAcomplexS(a) result(c)
    type(RAcomplexS),intent(in)::a
    type(RAcomplexS)::c
    type(RAcomplexS)::s
    type(RAcomplexS)::t
    include 'RAsincos.i90'
  end function cosRAcomplexS
  elemental function cosRAcomplexD(a) result(c)
    type(RAcomplexD),intent(in)::a
    type(RAcomplexD)::c
    type(RAcomplexD)::s
    type(RAcomplexD)::t
    include 'RAsincos.i90'
  end function cosRAcomplexD
end module RAcos