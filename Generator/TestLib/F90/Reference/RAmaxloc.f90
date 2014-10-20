! This file was generated by Rapsodia (see www.mcs.anl.gov/Rapsodia)
module RAmaxloc
  use RAprec
  use RAtypes
  implicit none
  interface maxloc
    module procedure maxlocRArealS1
    module procedure maxlocRArealD1
    module procedure maxlocRArealS2
    module procedure maxlocRArealD2
    module procedure maxlocRArealS3
    module procedure maxlocRArealD3
    module procedure maxlocRArealS4
    module procedure maxlocRArealD4
    module procedure maxlocRArealS5
    module procedure maxlocRArealD5
    module procedure maxlocRArealS6
    module procedure maxlocRArealD6
    module procedure maxlocRArealS7
    module procedure maxlocRArealD7
  end interface maxloc
contains 
  function maxlocRArealS1(a) result(r)
    type(RArealS),intent(in)::a(:)
    integer::r(1)
    include 'RAmaxloc.i90'
  end function maxlocRArealS1
  function maxlocRArealD1(a) result(r)
    type(RArealD),intent(in)::a(:)
    integer::r(1)
    include 'RAmaxloc.i90'
  end function maxlocRArealD1
  function maxlocRArealS2(a) result(r)
    type(RArealS),intent(in)::a(:,:)
    integer::r(2)
    include 'RAmaxloc.i90'
  end function maxlocRArealS2
  function maxlocRArealD2(a) result(r)
    type(RArealD),intent(in)::a(:,:)
    integer::r(2)
    include 'RAmaxloc.i90'
  end function maxlocRArealD2
  function maxlocRArealS3(a) result(r)
    type(RArealS),intent(in)::a(:,:,:)
    integer::r(3)
    include 'RAmaxloc.i90'
  end function maxlocRArealS3
  function maxlocRArealD3(a) result(r)
    type(RArealD),intent(in)::a(:,:,:)
    integer::r(3)
    include 'RAmaxloc.i90'
  end function maxlocRArealD3
  function maxlocRArealS4(a) result(r)
    type(RArealS),intent(in)::a(:,:,:,:)
    integer::r(4)
    include 'RAmaxloc.i90'
  end function maxlocRArealS4
  function maxlocRArealD4(a) result(r)
    type(RArealD),intent(in)::a(:,:,:,:)
    integer::r(4)
    include 'RAmaxloc.i90'
  end function maxlocRArealD4
  function maxlocRArealS5(a) result(r)
    type(RArealS),intent(in)::a(:,:,:,:,:)
    integer::r(5)
    include 'RAmaxloc.i90'
  end function maxlocRArealS5
  function maxlocRArealD5(a) result(r)
    type(RArealD),intent(in)::a(:,:,:,:,:)
    integer::r(5)
    include 'RAmaxloc.i90'
  end function maxlocRArealD5
  function maxlocRArealS6(a) result(r)
    type(RArealS),intent(in)::a(:,:,:,:,:,:)
    integer::r(6)
    include 'RAmaxloc.i90'
  end function maxlocRArealS6
  function maxlocRArealD6(a) result(r)
    type(RArealD),intent(in)::a(:,:,:,:,:,:)
    integer::r(6)
    include 'RAmaxloc.i90'
  end function maxlocRArealD6
  function maxlocRArealS7(a) result(r)
    type(RArealS),intent(in)::a(:,:,:,:,:,:,:)
    integer::r(7)
    include 'RAmaxloc.i90'
  end function maxlocRArealS7
  function maxlocRArealD7(a) result(r)
    type(RArealD),intent(in)::a(:,:,:,:,:,:,:)
    integer::r(7)
    include 'RAmaxloc.i90'
  end function maxlocRArealD7
end module RAmaxloc
