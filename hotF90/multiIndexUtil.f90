!#########################################################
! This file is part of Rapsodia released under the LGPL. #
! The full COPYRIGHT notice can be found in the top      #
! level directory of the Rapsodia distribution           #
!#########################################################
module multiIndexUtil
  implicit none
  public :: & 
multiIndex, & 
setNumberOfIndexElements, & 
getNumberOfIndexElements, & 
setDegree, & 
getDegree, & 
setStartPosition, & 
getPosition, & 
getIndexCount, & 
getIndices, &
binomial, & 
indexBinomial, & 
computeIndexCount, & 
l1Norm, & 
l1NormOfDifference, & 
lessThanOrEqual

  integer,public,parameter::hotKind = kind(1.0D0)

  private :: &
makeIndices, & 
setLeadingDimension, & 
debugFlag

  logical :: debugFlag=.true.

  type multiIndex
     ! number of index elements
     integer :: myN=0 
     ! highest  index degree
     integer :: myD=0 
     ! number of Indexs,
     ! this is set when we make the indices
     integer :: myNumberOfIndices=0 
     ! index matrix (myN,myNumberOfIndices)
     integer, dimension(:,:), allocatable :: myIndices 
     ! index starting position from which we get the position
     integer :: myStartPosition = 0
  end type multiIndex

  interface setNumberOfIndexElements
     module procedure setNumberOfIndexElements_i
  end interface

  interface getNumberOfIndexElements
     module procedure getNumberOfIndexElements_i
  end interface

  interface setDegree
     module procedure setDegree_i
  end interface

  interface getDegree
     module procedure getDegree_i
  end interface

  interface setStartPosition
     module procedure setStartPosition_i
  end interface

  interface getPosition
     module procedure getPosition_i
  end interface

  interface getIndices
     module procedure getIndices_i
  end interface

  interface binomial
     module procedure binomial_i
     module procedure DBinomial_i
  end interface

  interface indexBinomial
     module procedure indexBinomial_i
     module procedure DIndexBinomial_i
  end interface

  interface l1Norm
     module procedure l1Norm_i
  end interface

  interface l1NormOfDifference
     module procedure l1NormOfDifference_i
  end interface

  interface lessThanOrEqual
     module procedure lessThanOrEqual_i
  end interface

  interface computeIndexCount
     module procedure computeIndexCount_i
  end interface

  interface makeIndices
     module procedure makeIndices_i
  end interface

  interface setLeadingDimension
     module procedure setLeadingDimension_i
  end interface

contains

  subroutine setNumberOfIndexElements_i(aMultiI,n)
    type(multiIndex), intent(inout) :: aMultiI
    integer, intent(in) :: n
    if (aMultiI%myN>0) stop 'number of index elements already set'
    aMultiI%myN=n
  end subroutine setNumberOfIndexElements_i

  integer function getNumberOfIndexElements_i(aMultiI)
    type(multiIndex), intent(in) :: aMultiI
    if (aMultiI%myN==0) stop 'number of index elements not set'
    getNumberOfIndexElements_i=aMultiI%myN
  end function getNumberOfIndexElements_i

  subroutine setDegree_i(aMultiI,d)
    type(multiIndex), intent(inout) :: aMultiI
    integer, intent(in) :: d
    if (aMultiI%myD>0) stop 'degree already set'
    aMultiI%myD=d
  end subroutine setDegree_i

  integer function getDegree_i(aMultiI)
    type(multiIndex), intent(in) :: aMultiI
    if (aMultiI%myN==0) stop 'degree not set'
    getDegree_i=aMultiI%myD
  end function getDegree_i

  subroutine setStartPosition_i(aMultiI,p)
    type(multiIndex), intent(inout) :: aMultiI
    integer, intent(in) :: p
    if (aMultiI%myStartPosition>0) stop 'start position already set'
    aMultiI%myStartPosition=p
  end subroutine setStartPosition_i

  integer function getPosition_i(aMultiI, i)
    type(multiIndex), intent(in) :: aMultiI
    integer, intent(in) :: i
    if (aMultiI%myStartPosition==0) stop 'start position not set'
    getPosition_i=aMultiI%myStartPosition+i-1
  end function getPosition_i

  subroutine getIndices_i(aMultiI,s)
    type(multiIndex), intent(inout) :: aMultiI
    integer, intent(out), dimension(:,:) :: s
    if (.not. allocated(aMultiI%myIndices)) call makeIndices(aMultiI)
    if (size(s,1)/=aMultiI%myN) stop 'wrong first dimension for second argument'
    if (size(s,2)/=aMultiI%myNumberOfIndices) stop 'wrong second dimension for second argument'
    s=aMultiI%myIndices
  end subroutine getIndices_i

  subroutine makeIndices_i(aMultiI)
    implicit none
    type(multiIndex), intent(inout) :: aMultiI
    integer n, d, i, currDir
    n=getNumberOfIndexElements(aMultiI)
    d=getDegree(aMultiI)
    allocate(aMultiI%myIndices(n,getIndexCount(aMultiI)))
    if (n==1) then 
       aMultiI%myIndices(1,1)=d
    else
       ! we pick the Indexs each with d_i, i=1,.n
       ! such that the sum over all d_i equals d
       currDir=1
       do i=0,d
          aMultiI%myIndices(1,currDir:currDir+computeIndexCount(n-1,d-i)-1)=i
          call setLeadingDimension_i(n-1,d-i,currDir,aMultiI%myIndices(2:,:))
       end do
    end if
  end subroutine makeIndices_i
       
  integer function binomial_i(a,b)
    implicit none
    integer, intent(in) :: a,b
    integer i
    binomial_i = 1
    do i=1,b
       binomial_i = (binomial_i*(a-i+1))/i; 
    end do
!    if (binomial_i==0) then 
!       print *, 'binomial zero return', a,b
!    end if
  end function binomial_i

  real(kind=hotKind) function DBinomial_i(a,s,b)
    implicit none
    integer, intent(in) :: a,b
    real(kind=hotKind), intent(in) :: s ! scaling factor
    real(kind=hotKind) :: sa
    integer i
    sa=s*a
    dbinomial_i = 1.0
    do i=1,b
       dbinomial_i = (dbinomial_i*(sa-i+1))/i; 
    end do
!    if (dbinomial_i==0) then 
!       print *, 'dbinomial zero return', a,s,b
!    end if
  end function DBinomial_i

  integer function indexBinomial_i(aMultiI1, index1, aMultiI2, index2)
    implicit none
    type(multiIndex), intent(inout) :: aMultiI1, aMultiI2
    integer, intent(in) :: index1,index2
    integer i
    if (debugFlag) then 
       if (.not. allocated(aMultiI1%myIndices)) call makeIndices(aMultiI1)
       if (.not. allocated(aMultiI2%myIndices)) call makeIndices(aMultiI2)
       if (aMultiI1%myN /= aMultiI2%myN) stop 'indexBinomial: element numbers do not match'
       if (aMultiI1%myNumberOfIndices<index1 .or. index1<1) stop 'indexBinomial: index 1 out of bounds'
       if (aMultiI2%myNumberOfIndices<index2 .or. index1<1) stop 'indexBinomial: index 2 out of bounds'
    end if
    indexBinomial_i = 1
    do i=1,aMultiI1%myN
       indexBinomial_i = indexBinomial_i*binomial(aMultiI1%myIndices(i,index1),aMultiI2%myIndices(i,index2))
    end do
!    if (indexBinomial_i == 0) then 
!       print*, aMultiI1%myIndices(:,index1), aMultiI2%myIndices(:,index2)
!       stop 'zero return'
!    end if
  end function indexBinomial_i

  real(kind=hotKind) function DIndexBinomial_i(aMultiI1, index1,s, aMultiI2, index2)
    implicit none
    type(multiIndex), intent(inout) :: aMultiI1, aMultiI2
    integer, intent(in) :: index1,index2
    real(kind=hotKind), intent(in):: s ! scaling factor
    integer i
    if (debugFlag) then 
       if (.not. allocated(aMultiI1%myIndices)) call makeIndices(aMultiI1)
       if (.not. allocated(aMultiI2%myIndices)) call makeIndices(aMultiI2)
       if (aMultiI1%myN /= aMultiI2%myN) stop 'DIndexBinomial: element numbers do not match'
       if (aMultiI1%myNumberOfIndices<index1 .or. index1<1) stop 'DIndexBinomial: index 1 out of bounds'
       if (aMultiI2%myNumberOfIndices<index2 .or. index1<1) stop 'DIndexBinomial: index 2 out of bounds'
    end if
    DIndexBinomial_i = 1
    do i=1,aMultiI1%myN
       DIndexBinomial_i = DIndexBinomial_i*binomial(aMultiI1%myIndices(i,index1),s,aMultiI2%myIndices(i,index2))
    end do
  end function DIndexBinomial_i

  integer function l1Norm_i(aMultiI, index)
    implicit none
    type(multiIndex), intent(inout) :: aMultiI
    integer, intent(in) :: index
    integer i
    if (debugFlag) then 
       if (.not. allocated(aMultiI%myIndices)) call makeIndices(aMultiI)
       if (aMultiI%myNumberOfIndices<index .or. index<1) stop 'index out of bounds'
    end if
    l1Norm_i = 0
    do i=1,aMultiI%myN
       l1Norm_i = l1Norm_i + aMultiI%myIndices(i,index)
    end do
  end function l1Norm_i
  
  integer function l1NormOfDifference_i(aMultiI1, index1, aMultiI2, index2)
    implicit none
    type(multiIndex), intent(inout) :: aMultiI1, aMultiI2
    integer, intent(in) :: index1,index2
    integer i
    if (debugFlag) then 
       if (.not. allocated(aMultiI1%myIndices)) call makeIndices(aMultiI1)
       if (.not. allocated(aMultiI2%myIndices)) call makeIndices(aMultiI2)
       if (aMultiI1%myN /= aMultiI2%myN) stop 'l1NormOfDifference_i: element numbers do not match'
       if (aMultiI1%myNumberOfIndices<index1 .or. index1<1) stop 'l1NormOfDifference_i: index 1 out of bounds'
       if (aMultiI2%myNumberOfIndices<index2 .or. index2<1) stop 'l1NormOfDifference_i: index 2 out of bounds'
    end if
    l1NormOfDifference_i = 0
    do i=1,aMultiI1%myN
       l1NormOfDifference_i = l1NormOfDifference_i + aMultiI1%myIndices(i,index1)-aMultiI2%myIndices(i,index2)
    end do
  end function l1NormOfDifference_i

  logical function lessThanOrEqual_i(aMultiI1, index1, aMultiI2, index2)
    implicit none
    type(multiIndex), intent(inout) :: aMultiI1, aMultiI2
    integer, intent(in) :: index1,index2
    integer i
    if (debugFlag) then 
       if (.not. allocated(aMultiI1%myIndices)) call makeIndices(aMultiI1)
       if (.not. allocated(aMultiI2%myIndices)) call makeIndices(aMultiI2)
       if (aMultiI1%myN /= aMultiI2%myN) stop 'lessThanOrEqual_i: element numbers do not match'
       if (aMultiI1%myNumberOfIndices<index1 .or. index1<1) stop 'lessThanOrEqual_i: index 1 out of bounds'
       if (aMultiI2%myNumberOfIndices<index2 .or. index2<1) stop 'lessThanOrEqual_i: index 2 out of bounds'
    end if
    lessThanOrEqual_i = .true.
    do i=1,aMultiI1%myN
       if ((aMultiI1%myIndices(i,index1))>(aMultiI2%myIndices(i,index2))) then 
          lessThanOrEqual_i=.false.
          exit
       end if
    end do
  end function lessThanOrEqual_i
  
  integer function computeIndexCount_i(n,d)
    implicit none
    integer, intent(in) :: n,d
    computeIndexCount_i=binomial(n+d-1,d)
  end function computeIndexCount_i

  integer function getIndexCount(aMultiI)
    implicit none
    type(multiIndex), intent(inout) :: aMultiI
    if (aMultiI%myNumberOfIndices==0) then 
       aMultiI%myNumberOfIndices=computeIndexCount(getNumberOfIndexElements(aMultiI),getDegree(aMultiI))
    end if
    getIndexCount=aMultiI%myNumberOfIndices
  end function getIndexCount

  recursive subroutine setLeadingDimension_i(n,d,currDir,S)
    integer, intent(in) :: n ! (current) number of index elements
    integer, intent(in) :: d ! (current) highest  degree
    integer, intent(inout) :: currDir ! the current Index
    integer, intent(inout), dimension(:,:) :: S ! the seed matrix
    integer i
!    print * , 'setLeadingDimension called with', n, ',', d, ',',currDir
    if (n>1) then 
       do i=0,d
          S(1,currDir:currDir+computeIndexCount(n-1,d-i)-1)=i
          call setLeadingDimension_i(n-1,d-i,currDir,S(2:,:))
       end do
    else
       S(1,currDir)=d
       currDir=currDir+1
    end if
  end subroutine setLeadingDimension_i

end module
