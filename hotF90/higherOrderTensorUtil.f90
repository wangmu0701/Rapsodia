!#########################################################
! This file is part of Rapsodia released under the LGPL. #
! The full COPYRIGHT notice can be found in the top      #
! level directory of the Rapsodia distribution           #
!#########################################################

!>
!!  \mainpage Rapsodia (hotF90)
!!  \author Isabelle Charpentier and Jean Utke
!!    
!!  \section intro Introduction
!!  
!! Rapsodia = <b>rap</b>ide <b>s</b>urcharge d'<b>o</b>p&eacute;rateur pour la <b>di</b>ff&eacute;rentiation <b>a</b>utomatique.
!!
!! hotCpp   = <b>h</b>igher-<b>o</b>rder <b>t</b>ensor interpolation implemented in <b>C++</b>
!! 
!! hotF90   = <b>h</b>igher-<b>o</b>rder <b>t</b>ensor interpolation implemented in <b>F90</b>
!! 
!! Rapsodia is a tool for the efficient computation of higher order derivative tensors. 
!! It consists of two parts. 
!! <ol>
!! <li> A Python-based generator producing C++ or Fortran code for the forward propagation  of univariate Taylor polynomials.
!! This code yields efficiency gains via explcitly unrolled loops for a fixed derivative order and number of directions.
!!
!! <li> Implementations of the algorithm to interpolate derivative tensor entries from univariate 
!! Taylor coefficients in C++ and Fortran  
!! </ol> 
!! This part of the documentation covers the F90 implementation of the higher-order tensor interpolation.
!!

module higherOrderTensorUtil
  use multiIndexUtil
  implicit none
  public :: & 
higherOrderTensor, & 
setNumberOfIndependents, & 
getNumberOfIndependents, & 
setHighestDerivativeDegree, & 
getHighestDerivativeDegree, & 
getDirectionCount, & 
getSeedMatrix, & 
setTaylorCoefficients, & 
getCompressedTensor, &
makeInterpolationCoefficients, &
reset

  private :: &
makeMultiIndices

  type higherOrderTensor
     !> number of Independents
     integer :: myN=0 
     !> highest derivative degree
     integer :: myD=0 
     !> number of directions
     integer :: myNumberOfDirections=0 
     !> all the multiIndices up to degree myD
     type(multiIndex), dimension(:), allocatable :: myMultiIndices 
     !> taylor coefficients computed by the user; 
     !! first dimension is myD; 
     !! second dimension is myNumberOfDirections
     real(kind=hotKind), dimension(:,:), allocatable :: myTaylorCoefficients
     !> interpolation coefficients (computed once by makeInterpolationCoefficients)
     real(kind=hotKind), dimension(:,:), allocatable :: myInterpolationCoefficients
     !> total index counter
     integer :: myIndexCounter=0 
  end type higherOrderTensor

  interface setNumberOfIndependents
     module procedure setNumberOfIndependents_i
  end interface

  interface getNumberOfIndependents
     module procedure getNumberOfIndependents_i
  end interface

  interface setHighestDerivativeDegree
     module procedure setHighestDerivativeDegree_i
  end interface

  interface getHighestDerivativeDegree
     module procedure getHighestDerivativeDegree_i
  end interface

  interface getSeedMatrix
     module procedure getSeedMatrix_i
  end interface

  interface setTaylorCoefficients
     module procedure setTaylorCoefficients_i
  end interface

  interface getCompressedTensor
     module procedure getCompressedTensor_i
  end interface

  interface makeMultiIndices
     module procedure makeMultiIndices_i
  end interface

  interface makeInterpolationCoefficients
     module procedure makeInterpolationCoefficients_i
  end interface

  interface reset
     module procedure reset_i
  end interface

contains

  subroutine setNumberOfIndependents_i(T,n)
    type(higherOrderTensor), intent(inout) :: T
    integer, intent(in) :: n
    if (T%myN>0) stop 'number of independents already set'
    T%myN=n
  end subroutine setNumberOfIndependents_i

  integer function getNumberOfIndependents_i(T)
    type(higherOrderTensor), intent(in) :: T
    if (T%myN==0) stop 'number of independents not set'
    getNumberOfIndependents_i=T%myN
  end function getNumberOfIndependents_i

  subroutine setHighestDerivativeDegree_i(T,d)
    type(higherOrderTensor), intent(inout) :: T
    integer, intent(in) :: d
    if (T%myD>0) stop 'highest derivative degree already set'
    T%myD=d
  end subroutine setHighestDerivativeDegree_i

  integer function getHighestDerivativeDegree_i(T)
    type(higherOrderTensor), intent(in) :: T
    if (T%myN==0) stop 'highest derivative degree not set'
    getHighestDerivativeDegree_i=T%myD
  end function getHighestDerivativeDegree_i

  subroutine setTaylorCoefficients_i(T,taylorCoefficients)
    type(higherOrderTensor), intent(inout) :: T
    real(kind=hotKind), intent(in), dimension(:,:) :: taylorCoefficients
    if (.not. allocated(T%myTaylorCoefficients)) then 
       allocate(T%myTaylorCoefficients(T%myD,getDirectionCount(T)))
    end if
    if (size(taylorCoefficients,1) /= T%myD) stop 'wrong first dimension of second argument'
    if (size(taylorCoefficients,2) /= getDirectionCount(T)) stop 'wrong second dimension of second argument'
    T%myTaylorCoefficients=taylorCoefficients
  end subroutine setTaylorCoefficients_i

  subroutine getCompressedTensor_i(T,tensorOrder,compressedTensor)
    type(higherOrderTensor), intent(inout) :: T
    integer, intent(in) :: tensorOrder
    ! dimension is the number of multiindices for the given tensororder
    real(kind=hotKind), intent(inout), dimension(:) :: compressedTensor
    integer :: i, j
    if (.not. allocated(T%myInterpolationCoefficients)) call makeInterpolationCoefficients(T)
    do i=1,getIndexCount(T%myMultiIndices(tensorOrder))
       compressedTensor(i)=0.0D0
       do j=1,getIndexCount(T%myMultiIndices(T%myD))
          compressedTensor(i)=compressedTensor(i)+ & 
T%myTaylorCoefficients(tensorOrder,j) * T%myInterpolationCoefficients(getPosition(T%myMultiIndices(tensorOrder),i),j)
       end do
    end do
  end subroutine getCompressedTensor_i

  subroutine getSeedMatrix_i(T,s)
    type(higherOrderTensor), intent(inout) :: T
    integer, intent(out), dimension(:,:) :: s
    if (.not. allocated(T%myMultiIndices)) call makeMultiIndices(T)
    call getIndices(T%myMultiIndices(T%myD),s)
  end subroutine getSeedMatrix_i

  subroutine makeMultiIndices_i(T)
    implicit none
    type(higherOrderTensor), intent(inout) :: T
    integer :: n, d, i
    n=getNumberOfIndependents(T)
    d=getHighestDerivativeDegree(T)
    T%myIndexCounter=1
    allocate(T%myMultiIndices(d))
    ! we pick the directions each with d_i, i=1,.n
    ! such that the sum over all d_i equals d
    do i=1,d
       call setNumberOfIndexElements(T%myMultiIndices(i),n)
       call setDegree(T%myMultiIndices(i),i)
       call setStartPosition(T%myMultiIndices(i),T%myIndexCounter)
       T%myIndexCounter=T%myIndexCounter+getIndexCount(T%myMultiIndices(i))
    end do
  end subroutine makeMultiIndices_i

  subroutine makeInterpolationCoefficients_i(T)
    implicit none
    type(higherOrderTensor), intent(inout) :: T
    integer n, d, coefficientDimension, in,id, j, kd, kn,  l1Ofk,factor
    real(kind=hotKind) :: coefficient
    n=getNumberOfIndependents(T)
    d=getHighestDerivativeDegree(T)
    if (T%myIndexCounter == 0) call makeMultiIndices(T)
    ! by this time T%myIndexCounter counts all needed positions plus 1
    coefficientDimension=T%myIndexCounter-1
    allocate(T%myInterpolationCoefficients(coefficientDimension,getIndexCount(T%myMultiIndices(d))))
    do id=1,d
       do in=1,getIndexCount(T%myMultiIndices(id))
          do j=1,getIndexCount(T%myMultiIndices(d))
             ! now do the loop for the sum where
             ! we need to find all the kd/kn indices smaller than the id/in index
             coefficient=0.0D0
             do kd=1,id ! we don't need to look past degree id
                do kn=1,getIndexCount(T%myMultiIndices(kd))
                   ! obviously we still need to check <=
                   if (lessThanOrEqual(T%myMultiIndices(kd),kn,T%myMultiIndices(id),in)) then 
                      l1Ofk=l1Norm(T%myMultiIndices(kd),kn)
                      if (mod(l1NormOfDifference(T%myMultiIndices(id),in,T%myMultiIndices(kd),kn),2)==0) then
                         factor=1
                      else
                         factor=-1
                      end if
                      coefficient=coefficient+& 
factor * &
indexBinomial(T%myMultiIndices(id),in,T%myMultiIndices(kd),kn)* &
indexBinomial(T%myMultiIndices(kd),kn,REAL((d*1.0D0)/(l1Ofk*1.0D0),kind=hotKind),T%myMultiIndices(d),j) * &
((l1Ofk*1.0D0)/(d*1.0D0))**l1Norm(T%myMultiIndices(id),in)
                   end if ! was <=
                end do ! kn
             end do ! kd
             T%myInterpolationCoefficients(getPosition(T%myMultiIndices(id),in),j)=coefficient
          end do
       end do
    end do
!    do in=1,coefficientDimension
!      do j=1, getIndexCount(T%myMultiIndices(d))
!        print *,'c[',in,'][',j,']=', T%myInterpolationCoefficients(in,j)
!      end do
!   end do
  end subroutine makeInterpolationCoefficients_i
       
  integer function getDirectionCount(T)
    implicit none
    type(higherOrderTensor), intent(inout) :: T
    if (T%myNumberOfDirections==0) then 
       T%myNumberOfDirections=computeIndexCount(getNumberOfIndependents(T),getHighestDerivativeDegree(T))
    end if
    getDirectionCount=T%myNumberOfDirections
  end function getDirectionCount

  subroutine reset_i(T)
    implicit none
    type(higherOrderTensor), intent(inout) :: T
    T%myN=0 
    T%myD=0 
    T%myNumberOfDirections=0 
    if (allocated(T%myMultiIndices)) deallocate(T%myMultiIndices)
    if (allocated(T%myTaylorCoefficients)) deallocate(T%myTaylorCoefficients)
    if (allocated(T%myInterpolationCoefficients)) deallocate(T%myInterpolationCoefficients)
    T%myIndexCounter=0 
  end subroutine reset_i

end module
