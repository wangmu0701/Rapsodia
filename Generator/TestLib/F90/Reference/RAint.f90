! This file was generated by Rapsodia (see www.mcs.anl.gov/Rapsodia)
module RAint
  use RAprec
  use RAtypes
  implicit none
  interface int
    module procedure intRArealS
    module procedure intRArealD
    module procedure intRAcomplexS
    module procedure intRAcomplexD
  end interface int
contains 
  elemental function intRArealS(a) result(r)
    type(RArealS),intent(in)::a
    integer::r
    include 'RAint.i90'
  end function intRArealS
  elemental function intRArealD(a) result(r)
    type(RArealD),intent(in)::a
    integer::r
    include 'RAint.i90'
  end function intRArealD
  elemental function intRAcomplexS(a) result(r)
    type(RAcomplexS),intent(in)::a
    integer::r
    include 'RAint.i90'
  end function intRAcomplexS
  elemental function intRAcomplexD(a) result(r)
    type(RAcomplexD),intent(in)::a
    integer::r
    include 'RAint.i90'
  end function intRAcomplexD
end module RAint
