! This file was generated by Rapsodia (see www.mcs.anl.gov/Rapsodia)
module RAtypes
  use RAprec
  implicit none
  integer,parameter::arrSz = 31
  public::RArealS
  public::RArealD
  public::RAcomplexS
  public::RAcomplexD
  public::RAset
  interface RAset
    module procedure setRArealS
    module procedure setRArealD
    module procedure setRAcomplexS
    module procedure setRAcomplexD
  end interface RAset
  public::RAget
  interface RAget
    module procedure getRArealS
    module procedure getRArealD
    module procedure getRAcomplexS
    module procedure getRAcomplexD
  end interface RAget
  public::RAtoArray
  interface RAtoArray
    module procedure toArrayRArealS
    module procedure toArrayRArealD
    module procedure toArrayRAcomplexS
    module procedure toArrayRAcomplexD
  end interface RAtoArray
  public::RAfromArray
  interface RAfromArray
    module procedure fromArrayRArealS
    module procedure fromArrayRArealD
    module procedure fromArrayRAcomplexS
    module procedure fromArrayRAcomplexD
  end interface RAfromArray
  type RArealS
    real(kind=RAsKind)::v
    real(kind=RAsKind)::d1_1
    real(kind=RAsKind)::d1_2
    real(kind=RAsKind)::d1_3
    real(kind=RAsKind)::d1_4
    real(kind=RAsKind)::d1_5
    real(kind=RAsKind)::d1_6
    real(kind=RAsKind)::d1_7
    real(kind=RAsKind)::d1_8
    real(kind=RAsKind)::d1_9
    real(kind=RAsKind)::d1_10
    real(kind=RAsKind)::d2_1
    real(kind=RAsKind)::d2_2
    real(kind=RAsKind)::d2_3
    real(kind=RAsKind)::d2_4
    real(kind=RAsKind)::d2_5
    real(kind=RAsKind)::d2_6
    real(kind=RAsKind)::d2_7
    real(kind=RAsKind)::d2_8
    real(kind=RAsKind)::d2_9
    real(kind=RAsKind)::d2_10
    real(kind=RAsKind)::d3_1
    real(kind=RAsKind)::d3_2
    real(kind=RAsKind)::d3_3
    real(kind=RAsKind)::d3_4
    real(kind=RAsKind)::d3_5
    real(kind=RAsKind)::d3_6
    real(kind=RAsKind)::d3_7
    real(kind=RAsKind)::d3_8
    real(kind=RAsKind)::d3_9
    real(kind=RAsKind)::d3_10
  end type RArealS
  type RArealD
    real(kind=RAdKind)::v
    real(kind=RAdKind)::d1_1
    real(kind=RAdKind)::d1_2
    real(kind=RAdKind)::d1_3
    real(kind=RAdKind)::d1_4
    real(kind=RAdKind)::d1_5
    real(kind=RAdKind)::d1_6
    real(kind=RAdKind)::d1_7
    real(kind=RAdKind)::d1_8
    real(kind=RAdKind)::d1_9
    real(kind=RAdKind)::d1_10
    real(kind=RAdKind)::d2_1
    real(kind=RAdKind)::d2_2
    real(kind=RAdKind)::d2_3
    real(kind=RAdKind)::d2_4
    real(kind=RAdKind)::d2_5
    real(kind=RAdKind)::d2_6
    real(kind=RAdKind)::d2_7
    real(kind=RAdKind)::d2_8
    real(kind=RAdKind)::d2_9
    real(kind=RAdKind)::d2_10
    real(kind=RAdKind)::d3_1
    real(kind=RAdKind)::d3_2
    real(kind=RAdKind)::d3_3
    real(kind=RAdKind)::d3_4
    real(kind=RAdKind)::d3_5
    real(kind=RAdKind)::d3_6
    real(kind=RAdKind)::d3_7
    real(kind=RAdKind)::d3_8
    real(kind=RAdKind)::d3_9
    real(kind=RAdKind)::d3_10
  end type RArealD
  type RAcomplexS
    complex(kind=RAsKind)::v
    complex(kind=RAsKind)::d1_1
    complex(kind=RAsKind)::d1_2
    complex(kind=RAsKind)::d1_3
    complex(kind=RAsKind)::d1_4
    complex(kind=RAsKind)::d1_5
    complex(kind=RAsKind)::d1_6
    complex(kind=RAsKind)::d1_7
    complex(kind=RAsKind)::d1_8
    complex(kind=RAsKind)::d1_9
    complex(kind=RAsKind)::d1_10
    complex(kind=RAsKind)::d2_1
    complex(kind=RAsKind)::d2_2
    complex(kind=RAsKind)::d2_3
    complex(kind=RAsKind)::d2_4
    complex(kind=RAsKind)::d2_5
    complex(kind=RAsKind)::d2_6
    complex(kind=RAsKind)::d2_7
    complex(kind=RAsKind)::d2_8
    complex(kind=RAsKind)::d2_9
    complex(kind=RAsKind)::d2_10
    complex(kind=RAsKind)::d3_1
    complex(kind=RAsKind)::d3_2
    complex(kind=RAsKind)::d3_3
    complex(kind=RAsKind)::d3_4
    complex(kind=RAsKind)::d3_5
    complex(kind=RAsKind)::d3_6
    complex(kind=RAsKind)::d3_7
    complex(kind=RAsKind)::d3_8
    complex(kind=RAsKind)::d3_9
    complex(kind=RAsKind)::d3_10
  end type RAcomplexS
  type RAcomplexD
    complex(kind=RAdKind)::v
    complex(kind=RAdKind)::d1_1
    complex(kind=RAdKind)::d1_2
    complex(kind=RAdKind)::d1_3
    complex(kind=RAdKind)::d1_4
    complex(kind=RAdKind)::d1_5
    complex(kind=RAdKind)::d1_6
    complex(kind=RAdKind)::d1_7
    complex(kind=RAdKind)::d1_8
    complex(kind=RAdKind)::d1_9
    complex(kind=RAdKind)::d1_10
    complex(kind=RAdKind)::d2_1
    complex(kind=RAdKind)::d2_2
    complex(kind=RAdKind)::d2_3
    complex(kind=RAdKind)::d2_4
    complex(kind=RAdKind)::d2_5
    complex(kind=RAdKind)::d2_6
    complex(kind=RAdKind)::d2_7
    complex(kind=RAdKind)::d2_8
    complex(kind=RAdKind)::d2_9
    complex(kind=RAdKind)::d2_10
    complex(kind=RAdKind)::d3_1
    complex(kind=RAdKind)::d3_2
    complex(kind=RAdKind)::d3_3
    complex(kind=RAdKind)::d3_4
    complex(kind=RAdKind)::d3_5
    complex(kind=RAdKind)::d3_6
    complex(kind=RAdKind)::d3_7
    complex(kind=RAdKind)::d3_8
    complex(kind=RAdKind)::d3_9
    complex(kind=RAdKind)::d3_10
  end type RAcomplexD
  public::makeFPE
  interface makeFPE
    module procedure makeFPE_i
  end interface makeFPE
contains 
  elemental function makeFPE_i(n,d) result(r)
    real,intent(in)::n
    real,intent(in)::d
    real::r
    r=n / d
  end function makeFPE_i
  subroutine setRArealS(active,direction,degree,passive)
    type(RArealS),intent(inout)::active
    integer,intent(in)::direction
    integer,intent(in)::degree
    real(kind=RAsKind),intent(in)::passive
    include 'RAset.i90'
  end subroutine setRArealS
  subroutine setRArealD(active,direction,degree,passive)
    type(RArealD),intent(inout)::active
    integer,intent(in)::direction
    integer,intent(in)::degree
    real(kind=RAdKind),intent(in)::passive
    include 'RAset.i90'
  end subroutine setRArealD
  subroutine setRAcomplexS(active,direction,degree,passive)
    type(RAcomplexS),intent(inout)::active
    integer,intent(in)::direction
    integer,intent(in)::degree
    complex(kind=RAsKind),intent(in)::passive
    include 'RAset.i90'
  end subroutine setRAcomplexS
  subroutine setRAcomplexD(active,direction,degree,passive)
    type(RAcomplexD),intent(inout)::active
    integer,intent(in)::direction
    integer,intent(in)::degree
    complex(kind=RAdKind),intent(in)::passive
    include 'RAset.i90'
  end subroutine setRAcomplexD
  subroutine getRArealS(active,direction,degree,passive)
    type(RArealS),intent(inout)::active
    integer,intent(in)::direction
    integer,intent(in)::degree
    real(kind=RAsKind),intent(out)::passive
    include 'RAget.i90'
  end subroutine getRArealS
  subroutine getRArealD(active,direction,degree,passive)
    type(RArealD),intent(inout)::active
    integer,intent(in)::direction
    integer,intent(in)::degree
    real(kind=RAdKind),intent(out)::passive
    include 'RAget.i90'
  end subroutine getRArealD
  subroutine getRAcomplexS(active,direction,degree,passive)
    type(RAcomplexS),intent(inout)::active
    integer,intent(in)::direction
    integer,intent(in)::degree
    complex(kind=RAsKind),intent(out)::passive
    include 'RAget.i90'
  end subroutine getRAcomplexS
  subroutine getRAcomplexD(active,direction,degree,passive)
    type(RAcomplexD),intent(inout)::active
    integer,intent(in)::direction
    integer,intent(in)::degree
    complex(kind=RAdKind),intent(out)::passive
    include 'RAget.i90'
  end subroutine getRAcomplexD
  subroutine toArrayRArealS(active,arr)
    type(RArealS),intent(in)::active
    real(kind=RAsKind),intent(out)::arr(arrSz)
    include 'RAtoArray.i90'
  end subroutine toArrayRArealS
  subroutine toArrayRArealD(active,arr)
    type(RArealD),intent(in)::active
    real(kind=RAdKind),intent(out)::arr(arrSz)
    include 'RAtoArray.i90'
  end subroutine toArrayRArealD
  subroutine toArrayRAcomplexS(active,arr)
    type(RAcomplexS),intent(in)::active
    complex(kind=RAsKind),intent(out)::arr(arrSz)
    include 'RAtoArray.i90'
  end subroutine toArrayRAcomplexS
  subroutine toArrayRAcomplexD(active,arr)
    type(RAcomplexD),intent(in)::active
    complex(kind=RAdKind),intent(out)::arr(arrSz)
    include 'RAtoArray.i90'
  end subroutine toArrayRAcomplexD
  subroutine fromArrayRArealS(active,arr)
    type(RArealS),intent(out)::active
    real(kind=RAsKind),intent(in)::arr(arrSz)
    include 'RAfromArray.i90'
  end subroutine fromArrayRArealS
  subroutine fromArrayRArealD(active,arr)
    type(RArealD),intent(out)::active
    real(kind=RAdKind),intent(in)::arr(arrSz)
    include 'RAfromArray.i90'
  end subroutine fromArrayRArealD
  subroutine fromArrayRAcomplexS(active,arr)
    type(RAcomplexS),intent(out)::active
    complex(kind=RAsKind),intent(in)::arr(arrSz)
    include 'RAfromArray.i90'
  end subroutine fromArrayRAcomplexS
  subroutine fromArrayRAcomplexD(active,arr)
    type(RAcomplexD),intent(out)::active
    complex(kind=RAdKind),intent(in)::arr(arrSz)
    include 'RAfromArray.i90'
  end subroutine fromArrayRAcomplexD
end module RAtypes
