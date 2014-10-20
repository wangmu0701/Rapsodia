! This file was generated by Rapsodia (see www.mcs.anl.gov/Rapsodia)
module RAlt
  use RAprec
  use RAtypes
  implicit none
  interface operator(<)
    module procedure ltRArealSRArealS
    module procedure ltRArealSRArealD
    module procedure ltRArealDRArealS
    module procedure ltRArealDRArealD
    module procedure ltRArealSinteger
    module procedure ltRArealSrealS
    module procedure ltRArealSrealD
    module procedure ltRArealDinteger
    module procedure ltRArealDrealS
    module procedure ltRArealDrealD
    module procedure ltintegerRArealS
    module procedure ltintegerRArealD
    module procedure ltrealSRArealS
    module procedure ltrealSRArealD
    module procedure ltrealDRArealS
    module procedure ltrealDRArealD
  end interface 
contains 
  elemental function ltRArealSRArealS(a,b) result(r)
    type(RArealS),intent(in)::a
    type(RArealS),intent(in)::b
    logical::r
    include 'RAltAA.i90'
  end function ltRArealSRArealS
  elemental function ltRArealSRArealD(a,b) result(r)
    type(RArealS),intent(in)::a
    type(RArealD),intent(in)::b
    logical::r
    include 'RAltAA.i90'
  end function ltRArealSRArealD
  elemental function ltRArealDRArealS(a,b) result(r)
    type(RArealD),intent(in)::a
    type(RArealS),intent(in)::b
    logical::r
    include 'RAltAA.i90'
  end function ltRArealDRArealS
  elemental function ltRArealDRArealD(a,b) result(r)
    type(RArealD),intent(in)::a
    type(RArealD),intent(in)::b
    logical::r
    include 'RAltAA.i90'
  end function ltRArealDRArealD
  elemental function ltRArealSinteger(a,b) result(r)
    type(RArealS),intent(in)::a
    integer,intent(in)::b
    logical::r
    include 'RAltAP.i90'
  end function ltRArealSinteger
  elemental function ltRArealSrealS(a,b) result(r)
    type(RArealS),intent(in)::a
    real(kind=RAsKind),intent(in)::b
    logical::r
    include 'RAltAP.i90'
  end function ltRArealSrealS
  elemental function ltRArealSrealD(a,b) result(r)
    type(RArealS),intent(in)::a
    real(kind=RAdKind),intent(in)::b
    logical::r
    include 'RAltAP.i90'
  end function ltRArealSrealD
  elemental function ltRArealDinteger(a,b) result(r)
    type(RArealD),intent(in)::a
    integer,intent(in)::b
    logical::r
    include 'RAltAP.i90'
  end function ltRArealDinteger
  elemental function ltRArealDrealS(a,b) result(r)
    type(RArealD),intent(in)::a
    real(kind=RAsKind),intent(in)::b
    logical::r
    include 'RAltAP.i90'
  end function ltRArealDrealS
  elemental function ltRArealDrealD(a,b) result(r)
    type(RArealD),intent(in)::a
    real(kind=RAdKind),intent(in)::b
    logical::r
    include 'RAltAP.i90'
  end function ltRArealDrealD
  elemental function ltintegerRArealS(a,b) result(r)
    integer,intent(in)::a
    type(RArealS),intent(in)::b
    logical::r
    include 'RAltPA.i90'
  end function ltintegerRArealS
  elemental function ltintegerRArealD(a,b) result(r)
    integer,intent(in)::a
    type(RArealD),intent(in)::b
    logical::r
    include 'RAltPA.i90'
  end function ltintegerRArealD
  elemental function ltrealSRArealS(a,b) result(r)
    real(kind=RAsKind),intent(in)::a
    type(RArealS),intent(in)::b
    logical::r
    include 'RAltPA.i90'
  end function ltrealSRArealS
  elemental function ltrealSRArealD(a,b) result(r)
    real(kind=RAsKind),intent(in)::a
    type(RArealD),intent(in)::b
    logical::r
    include 'RAltPA.i90'
  end function ltrealSRArealD
  elemental function ltrealDRArealS(a,b) result(r)
    real(kind=RAdKind),intent(in)::a
    type(RArealS),intent(in)::b
    logical::r
    include 'RAltPA.i90'
  end function ltrealDRArealS
  elemental function ltrealDRArealD(a,b) result(r)
    real(kind=RAdKind),intent(in)::a
    type(RArealD),intent(in)::b
    logical::r
    include 'RAltPA.i90'
  end function ltrealDRArealD
end module RAlt
