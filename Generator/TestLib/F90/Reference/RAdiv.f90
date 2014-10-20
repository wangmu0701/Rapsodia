! This file was generated by Rapsodia (see www.mcs.anl.gov/Rapsodia)
module RAdiv
  use RAprec
  use RAtypes
  implicit none
  interface operator(/)
    module procedure divRArealSRArealS
    module procedure divRArealSRArealD
    module procedure divRArealSRAcomplexS
    module procedure divRArealSRAcomplexD
    module procedure divRArealDRArealS
    module procedure divRArealDRArealD
    module procedure divRArealDRAcomplexS
    module procedure divRArealDRAcomplexD
    module procedure divRAcomplexSRArealS
    module procedure divRAcomplexSRArealD
    module procedure divRAcomplexSRAcomplexS
    module procedure divRAcomplexSRAcomplexD
    module procedure divRAcomplexDRArealS
    module procedure divRAcomplexDRArealD
    module procedure divRAcomplexDRAcomplexS
    module procedure divRAcomplexDRAcomplexD
    module procedure divRArealSinteger
    module procedure divRArealSrealS
    module procedure divRArealSrealD
    module procedure divRArealScomplexS
    module procedure divRArealScomplexD
    module procedure divRArealDinteger
    module procedure divRArealDrealS
    module procedure divRArealDrealD
    module procedure divRArealDcomplexS
    module procedure divRArealDcomplexD
    module procedure divRAcomplexSinteger
    module procedure divRAcomplexSrealS
    module procedure divRAcomplexSrealD
    module procedure divRAcomplexScomplexS
    module procedure divRAcomplexScomplexD
    module procedure divRAcomplexDinteger
    module procedure divRAcomplexDrealS
    module procedure divRAcomplexDrealD
    module procedure divRAcomplexDcomplexS
    module procedure divRAcomplexDcomplexD
    module procedure divintegerRArealS
    module procedure divintegerRArealD
    module procedure divintegerRAcomplexS
    module procedure divintegerRAcomplexD
    module procedure divrealSRArealS
    module procedure divrealSRArealD
    module procedure divrealSRAcomplexS
    module procedure divrealSRAcomplexD
    module procedure divrealDRArealS
    module procedure divrealDRArealD
    module procedure divrealDRAcomplexS
    module procedure divrealDRAcomplexD
    module procedure divcomplexSRArealS
    module procedure divcomplexSRArealD
    module procedure divcomplexSRAcomplexS
    module procedure divcomplexSRAcomplexD
    module procedure divcomplexDRArealS
    module procedure divcomplexDRArealD
    module procedure divcomplexDRAcomplexS
    module procedure divcomplexDRAcomplexD
  end interface 
contains 
  elemental function divRArealSRArealS(a,b) result(r)
    type(RArealS),intent(in)::a
    type(RArealS),intent(in)::b
    type(RArealS)::r
    real(kind=RAsKind)::recip
    include 'RAdivAA.i90'
  end function divRArealSRArealS
  elemental function divRArealSRArealD(a,b) result(r)
    type(RArealS),intent(in)::a
    type(RArealD),intent(in)::b
    type(RArealD)::r
    real(kind=RAdKind)::recip
    include 'RAdivAA.i90'
  end function divRArealSRArealD
  elemental function divRArealSRAcomplexS(a,b) result(r)
    type(RArealS),intent(in)::a
    type(RAcomplexS),intent(in)::b
    type(RAcomplexS)::r
    complex(kind=RAsKind)::recip
    include 'RAdivAA.i90'
  end function divRArealSRAcomplexS
  elemental function divRArealSRAcomplexD(a,b) result(r)
    type(RArealS),intent(in)::a
    type(RAcomplexD),intent(in)::b
    type(RAcomplexD)::r
    complex(kind=RAdKind)::recip
    include 'RAdivAA.i90'
  end function divRArealSRAcomplexD
  elemental function divRArealDRArealS(a,b) result(r)
    type(RArealD),intent(in)::a
    type(RArealS),intent(in)::b
    type(RArealD)::r
    real(kind=RAdKind)::recip
    include 'RAdivAA.i90'
  end function divRArealDRArealS
  elemental function divRArealDRArealD(a,b) result(r)
    type(RArealD),intent(in)::a
    type(RArealD),intent(in)::b
    type(RArealD)::r
    real(kind=RAdKind)::recip
    include 'RAdivAA.i90'
  end function divRArealDRArealD
  elemental function divRArealDRAcomplexS(a,b) result(r)
    type(RArealD),intent(in)::a
    type(RAcomplexS),intent(in)::b
    type(RAcomplexD)::r
    complex(kind=RAdKind)::recip
    include 'RAdivAA.i90'
  end function divRArealDRAcomplexS
  elemental function divRArealDRAcomplexD(a,b) result(r)
    type(RArealD),intent(in)::a
    type(RAcomplexD),intent(in)::b
    type(RAcomplexD)::r
    complex(kind=RAdKind)::recip
    include 'RAdivAA.i90'
  end function divRArealDRAcomplexD
  elemental function divRAcomplexSRArealS(a,b) result(r)
    type(RAcomplexS),intent(in)::a
    type(RArealS),intent(in)::b
    type(RAcomplexS)::r
    complex(kind=RAsKind)::recip
    include 'RAdivAA.i90'
  end function divRAcomplexSRArealS
  elemental function divRAcomplexSRArealD(a,b) result(r)
    type(RAcomplexS),intent(in)::a
    type(RArealD),intent(in)::b
    type(RAcomplexD)::r
    complex(kind=RAdKind)::recip
    include 'RAdivAA.i90'
  end function divRAcomplexSRArealD
  elemental function divRAcomplexSRAcomplexS(a,b) result(r)
    type(RAcomplexS),intent(in)::a
    type(RAcomplexS),intent(in)::b
    type(RAcomplexS)::r
    complex(kind=RAsKind)::recip
    include 'RAdivAA.i90'
  end function divRAcomplexSRAcomplexS
  elemental function divRAcomplexSRAcomplexD(a,b) result(r)
    type(RAcomplexS),intent(in)::a
    type(RAcomplexD),intent(in)::b
    type(RAcomplexD)::r
    complex(kind=RAdKind)::recip
    include 'RAdivAA.i90'
  end function divRAcomplexSRAcomplexD
  elemental function divRAcomplexDRArealS(a,b) result(r)
    type(RAcomplexD),intent(in)::a
    type(RArealS),intent(in)::b
    type(RAcomplexD)::r
    complex(kind=RAdKind)::recip
    include 'RAdivAA.i90'
  end function divRAcomplexDRArealS
  elemental function divRAcomplexDRArealD(a,b) result(r)
    type(RAcomplexD),intent(in)::a
    type(RArealD),intent(in)::b
    type(RAcomplexD)::r
    complex(kind=RAdKind)::recip
    include 'RAdivAA.i90'
  end function divRAcomplexDRArealD
  elemental function divRAcomplexDRAcomplexS(a,b) result(r)
    type(RAcomplexD),intent(in)::a
    type(RAcomplexS),intent(in)::b
    type(RAcomplexD)::r
    complex(kind=RAdKind)::recip
    include 'RAdivAA.i90'
  end function divRAcomplexDRAcomplexS
  elemental function divRAcomplexDRAcomplexD(a,b) result(r)
    type(RAcomplexD),intent(in)::a
    type(RAcomplexD),intent(in)::b
    type(RAcomplexD)::r
    complex(kind=RAdKind)::recip
    include 'RAdivAA.i90'
  end function divRAcomplexDRAcomplexD
  elemental function divRArealSinteger(a,b) result(r)
    type(RArealS),intent(in)::a
    integer,intent(in)::b
    type(RArealS)::r
    include 'RAdivAP.i90'
  end function divRArealSinteger
  elemental function divRArealSrealS(a,b) result(r)
    type(RArealS),intent(in)::a
    real(kind=RAsKind),intent(in)::b
    type(RArealS)::r
    include 'RAdivAP.i90'
  end function divRArealSrealS
  elemental function divRArealSrealD(a,b) result(r)
    type(RArealS),intent(in)::a
    real(kind=RAdKind),intent(in)::b
    type(RArealD)::r
    include 'RAdivAP.i90'
  end function divRArealSrealD
  elemental function divRArealScomplexS(a,b) result(r)
    type(RArealS),intent(in)::a
    complex(kind=RAsKind),intent(in)::b
    type(RAcomplexS)::r
    include 'RAdivAP.i90'
  end function divRArealScomplexS
  elemental function divRArealScomplexD(a,b) result(r)
    type(RArealS),intent(in)::a
    complex(kind=RAdKind),intent(in)::b
    type(RAcomplexD)::r
    include 'RAdivAP.i90'
  end function divRArealScomplexD
  elemental function divRArealDinteger(a,b) result(r)
    type(RArealD),intent(in)::a
    integer,intent(in)::b
    type(RArealD)::r
    include 'RAdivAP.i90'
  end function divRArealDinteger
  elemental function divRArealDrealS(a,b) result(r)
    type(RArealD),intent(in)::a
    real(kind=RAsKind),intent(in)::b
    type(RArealD)::r
    include 'RAdivAP.i90'
  end function divRArealDrealS
  elemental function divRArealDrealD(a,b) result(r)
    type(RArealD),intent(in)::a
    real(kind=RAdKind),intent(in)::b
    type(RArealD)::r
    include 'RAdivAP.i90'
  end function divRArealDrealD
  elemental function divRArealDcomplexS(a,b) result(r)
    type(RArealD),intent(in)::a
    complex(kind=RAsKind),intent(in)::b
    type(RAcomplexD)::r
    include 'RAdivAP.i90'
  end function divRArealDcomplexS
  elemental function divRArealDcomplexD(a,b) result(r)
    type(RArealD),intent(in)::a
    complex(kind=RAdKind),intent(in)::b
    type(RAcomplexD)::r
    include 'RAdivAP.i90'
  end function divRArealDcomplexD
  elemental function divRAcomplexSinteger(a,b) result(r)
    type(RAcomplexS),intent(in)::a
    integer,intent(in)::b
    type(RAcomplexS)::r
    include 'RAdivAP.i90'
  end function divRAcomplexSinteger
  elemental function divRAcomplexSrealS(a,b) result(r)
    type(RAcomplexS),intent(in)::a
    real(kind=RAsKind),intent(in)::b
    type(RAcomplexS)::r
    include 'RAdivAP.i90'
  end function divRAcomplexSrealS
  elemental function divRAcomplexSrealD(a,b) result(r)
    type(RAcomplexS),intent(in)::a
    real(kind=RAdKind),intent(in)::b
    type(RAcomplexD)::r
    include 'RAdivAP.i90'
  end function divRAcomplexSrealD
  elemental function divRAcomplexScomplexS(a,b) result(r)
    type(RAcomplexS),intent(in)::a
    complex(kind=RAsKind),intent(in)::b
    type(RAcomplexS)::r
    include 'RAdivAP.i90'
  end function divRAcomplexScomplexS
  elemental function divRAcomplexScomplexD(a,b) result(r)
    type(RAcomplexS),intent(in)::a
    complex(kind=RAdKind),intent(in)::b
    type(RAcomplexD)::r
    include 'RAdivAP.i90'
  end function divRAcomplexScomplexD
  elemental function divRAcomplexDinteger(a,b) result(r)
    type(RAcomplexD),intent(in)::a
    integer,intent(in)::b
    type(RAcomplexD)::r
    include 'RAdivAP.i90'
  end function divRAcomplexDinteger
  elemental function divRAcomplexDrealS(a,b) result(r)
    type(RAcomplexD),intent(in)::a
    real(kind=RAsKind),intent(in)::b
    type(RAcomplexD)::r
    include 'RAdivAP.i90'
  end function divRAcomplexDrealS
  elemental function divRAcomplexDrealD(a,b) result(r)
    type(RAcomplexD),intent(in)::a
    real(kind=RAdKind),intent(in)::b
    type(RAcomplexD)::r
    include 'RAdivAP.i90'
  end function divRAcomplexDrealD
  elemental function divRAcomplexDcomplexS(a,b) result(r)
    type(RAcomplexD),intent(in)::a
    complex(kind=RAsKind),intent(in)::b
    type(RAcomplexD)::r
    include 'RAdivAP.i90'
  end function divRAcomplexDcomplexS
  elemental function divRAcomplexDcomplexD(a,b) result(r)
    type(RAcomplexD),intent(in)::a
    complex(kind=RAdKind),intent(in)::b
    type(RAcomplexD)::r
    include 'RAdivAP.i90'
  end function divRAcomplexDcomplexD
  elemental function divintegerRArealS(a,b) result(r)
    integer,intent(in)::a
    type(RArealS),intent(in)::b
    type(RArealS)::r
    include 'RAdivPA.i90'
  end function divintegerRArealS
  elemental function divintegerRArealD(a,b) result(r)
    integer,intent(in)::a
    type(RArealD),intent(in)::b
    type(RArealD)::r
    include 'RAdivPA.i90'
  end function divintegerRArealD
  elemental function divintegerRAcomplexS(a,b) result(r)
    integer,intent(in)::a
    type(RAcomplexS),intent(in)::b
    type(RAcomplexS)::r
    include 'RAdivPA.i90'
  end function divintegerRAcomplexS
  elemental function divintegerRAcomplexD(a,b) result(r)
    integer,intent(in)::a
    type(RAcomplexD),intent(in)::b
    type(RAcomplexD)::r
    include 'RAdivPA.i90'
  end function divintegerRAcomplexD
  elemental function divrealSRArealS(a,b) result(r)
    real(kind=RAsKind),intent(in)::a
    type(RArealS),intent(in)::b
    type(RArealS)::r
    include 'RAdivPA.i90'
  end function divrealSRArealS
  elemental function divrealSRArealD(a,b) result(r)
    real(kind=RAsKind),intent(in)::a
    type(RArealD),intent(in)::b
    type(RArealD)::r
    include 'RAdivPA.i90'
  end function divrealSRArealD
  elemental function divrealSRAcomplexS(a,b) result(r)
    real(kind=RAsKind),intent(in)::a
    type(RAcomplexS),intent(in)::b
    type(RAcomplexS)::r
    include 'RAdivPA.i90'
  end function divrealSRAcomplexS
  elemental function divrealSRAcomplexD(a,b) result(r)
    real(kind=RAsKind),intent(in)::a
    type(RAcomplexD),intent(in)::b
    type(RAcomplexD)::r
    include 'RAdivPA.i90'
  end function divrealSRAcomplexD
  elemental function divrealDRArealS(a,b) result(r)
    real(kind=RAdKind),intent(in)::a
    type(RArealS),intent(in)::b
    type(RArealD)::r
    include 'RAdivPA.i90'
  end function divrealDRArealS
  elemental function divrealDRArealD(a,b) result(r)
    real(kind=RAdKind),intent(in)::a
    type(RArealD),intent(in)::b
    type(RArealD)::r
    include 'RAdivPA.i90'
  end function divrealDRArealD
  elemental function divrealDRAcomplexS(a,b) result(r)
    real(kind=RAdKind),intent(in)::a
    type(RAcomplexS),intent(in)::b
    type(RAcomplexD)::r
    include 'RAdivPA.i90'
  end function divrealDRAcomplexS
  elemental function divrealDRAcomplexD(a,b) result(r)
    real(kind=RAdKind),intent(in)::a
    type(RAcomplexD),intent(in)::b
    type(RAcomplexD)::r
    include 'RAdivPA.i90'
  end function divrealDRAcomplexD
  elemental function divcomplexSRArealS(a,b) result(r)
    complex(kind=RAsKind),intent(in)::a
    type(RArealS),intent(in)::b
    type(RAcomplexS)::r
    include 'RAdivPA.i90'
  end function divcomplexSRArealS
  elemental function divcomplexSRArealD(a,b) result(r)
    complex(kind=RAsKind),intent(in)::a
    type(RArealD),intent(in)::b
    type(RAcomplexD)::r
    include 'RAdivPA.i90'
  end function divcomplexSRArealD
  elemental function divcomplexSRAcomplexS(a,b) result(r)
    complex(kind=RAsKind),intent(in)::a
    type(RAcomplexS),intent(in)::b
    type(RAcomplexS)::r
    include 'RAdivPA.i90'
  end function divcomplexSRAcomplexS
  elemental function divcomplexSRAcomplexD(a,b) result(r)
    complex(kind=RAsKind),intent(in)::a
    type(RAcomplexD),intent(in)::b
    type(RAcomplexD)::r
    include 'RAdivPA.i90'
  end function divcomplexSRAcomplexD
  elemental function divcomplexDRArealS(a,b) result(r)
    complex(kind=RAdKind),intent(in)::a
    type(RArealS),intent(in)::b
    type(RAcomplexD)::r
    include 'RAdivPA.i90'
  end function divcomplexDRArealS
  elemental function divcomplexDRArealD(a,b) result(r)
    complex(kind=RAdKind),intent(in)::a
    type(RArealD),intent(in)::b
    type(RAcomplexD)::r
    include 'RAdivPA.i90'
  end function divcomplexDRArealD
  elemental function divcomplexDRAcomplexS(a,b) result(r)
    complex(kind=RAdKind),intent(in)::a
    type(RAcomplexS),intent(in)::b
    type(RAcomplexD)::r
    include 'RAdivPA.i90'
  end function divcomplexDRAcomplexS
  elemental function divcomplexDRAcomplexD(a,b) result(r)
    complex(kind=RAdKind),intent(in)::a
    type(RAcomplexD),intent(in)::b
    type(RAcomplexD)::r
    include 'RAdivPA.i90'
  end function divcomplexDRAcomplexD
end module RAdiv