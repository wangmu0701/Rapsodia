!#########################################################
! This file is part of Rapsodia released under the LGPL. #
! The full COPYRIGHT notice can be found in the top      #
! level directory of the Rapsodia distribution           #
!#########################################################
double precision function explicitSinProdTensorEntry(n,x,index)
  implicit none
  integer :: n
  double precision :: x(n)
  integer :: index(n)
  integer i
  explicitSinProdTensorEntry=1.0
  do i=1,n
     select case (MOD(index(i),4))
        case (0) 
           explicitSinProdTensorEntry=explicitSinProdTensorEntry*sin(x(i))
        case (1) 
           explicitSinProdTensorEntry=explicitSinProdTensorEntry*cos(x(i))
        case (2) 
           explicitSinProdTensorEntry=explicitSinProdTensorEntry*(-sin(x(i)))
        case (3) 
           explicitSinProdTensorEntry=explicitSinProdTensorEntry*(-cos(x(i)))
        case default
           stop 'no logic for this case'
     end select
  end do
end function explicitSinProdTensorEntry


program driver
  include 'RAinclude.i90'

  use higherOrderTensorUtil

  implicit none 

  external head


  type(RArealD), dimension(:), allocatable :: x
  real(kind=RAdKind), dimension(:), allocatable :: xv
  type(RArealD) :: y
  integer n,d
  type(higherOrderTensor) :: T,Thelper
  integer, dimension(:,:), allocatable :: SeedMatrix,SeedMatrixHelper
  real(kind=RAdKind), dimension(:,:), allocatable :: TaylorCoefficients
  real(kind=RAdKind), dimension(:), allocatable :: compressedTensor
  integer i,j,dirs,k
  real(kind=RAdKind), external :: explicitSinProdTensorEntry
  real(kind=RAdKind) :: entry
  n=3
  d=3
  allocate(x(n))
  allocate(xv(n))
  ! argument values
  do i=1,n
     xv(i)=1.0+.1*i
     x(i)=xv(i)
  end do
  ! initialize the tensor context
  call setNumberOfIndependents(T,n)
  call setHighestDerivativeDegree(T,d)
  dirs=getDirectionCount(T)
  allocate(SeedMatrix(n,dirs))
  call getSeedMatrix(T,SeedMatrix)
  do i=1,dirs
     do j=1,n
        call RAset(x(j),i,1,REAL(SeedMatrix(j,i),kind=RAdKind))
     end do
  end do
  ! compute the target function
  call head(x,y)
  ! transfer the taylor coefficients
  allocate(TaylorCoefficients(d,dirs))
  do i=1,d
     do j=1,dirs
        call RAget(y,j,i,TaylorCoefficients(i,j))
     end do
  end do
  call setTaylorCoefficients(T,TaylorCoefficients)
  do k=1, d
     write(*,'(A,I2)') "order: ", k
     call reset(Thelper)
     call setNumberOfIndependents(Thelper,n)
     call setHighestDerivativeDegree(Thelper,k)
     dirs=getDirectionCount(Thelper)
     if (allocated(compressedTensor)) deallocate(compressedTensor)
     allocate(compressedTensor(dirs))
     if (allocated(SeedMatrixHelper)) deallocate(SeedMatrixHelper)
     allocate(SeedMatrixHelper(n,dirs))
     call getSeedMatrix(Thelper,SeedMatrixHelper)
     ! compute the compressedTensor
     call getCompressedTensor(T,k,compressedTensor)
     do i=1,dirs
        entry=explicitSinProdTensorEntry(n,xv,SeedMatrixHelper(:,i))
        write(*,'(A)',ADVANCE='NO') 'T'
        do j=1,n
           write(*,'(A,I2,A)',ADVANCE='NO') '[',SeedMatrixHelper(j,i),']'
        end do
        write(*,'(A,E25.17E3)',ADVANCE='NO') ' ',compressedTensor(i)
        write(*,'(A,E25.17E3)',ADVANCE='NO') ' ?= ', entry
        if (abs(compressedTensor(i)-entry)>1.0D-6) then 
           write(*,'(A,E25.17E3)') ' diff is: ', abs(compressedTensor(i)-entry)
           stop 1
        else
           write(*,'(A)') ' ok'
        end if
     end do
  end do
  deallocate(compressedTensor)
  deallocate(TaylorCoefficients)
  deallocate(SeedMatrix)

end program driver


