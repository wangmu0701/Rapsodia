!#########################################################
! This file is part of Rapsodia released under the LGPL. #
! The full COPYRIGHT notice can be found in the top      #
! level directory of the Rapsodia distribution           #
!#########################################################
 program identities

  include 'RAinclude.i90'
  
  integer, parameter :: directions=2
  integer, parameter :: order=10

  integer testCase
  logical done, dumpedTestLine
  real(kind=RAdKind), dimension(directions,order) :: xCoeff,yCoeff
  type(RArealD) :: x,y
  real(kind=RAdKind) :: xp,yp, myEps=1.E-12
  character(len=50) :: testLine
  integer i,j

  ! the point at which we test
  xp=0.3
  
  ! keep the coefficient values for comparison
  do i=1,directions
    do j=1,order
      xCoeff(i,j)=0.0
    end do
    xCoeff(i,1)=REAL(i,kind=RAdKind)*0.3D0
  end do
 
  ! initialize the active input
  x=xp
  do i=1,directions
    do j=1,order
       call RAset(x,i,j,xCoeff(i,j))
    end do
  end do
 
  ! populate the coefficients
  ! with something nontrivial
  x=asin(x)

  done=.false.
  testCase=0

  ! run the identities
  do while (.not.done) 

   select case(testCase)
  
     case(0) 
        y=x
        ! print *, x
        ! print *, y
        testline='y=x'

     case(1) 
        y=x+x-x
        testline='y=x+x-x'

     case(2)
        y=-2+(2+((x+2)-2))
        testline='y=-2+(2+((x+2)-2))'

     case(3)
        y=(2*x)/2
        testline='y=(2*x)/2'

     case(4)
        y=(x*x)/x
        testline='y=(x*x)/x'

     case(5)
        y=sqrt(x*x)
        testline='y=sqrt(x*x)'

     case(6)
        y=sqrt(x**2)
        testline='y=sqrt(x**2)'

     case(7)
        y=log(exp(x))
        testline='y=log(exp(x))'

     case(8)
        y=(x**2)**(.5)
        testline='y=(x**2)**(.5)'

     case(9)
        y=(x**3)**(1.0D0/3.0D0)
        testline='y=(x**3)**(1.0D0/3.0D0)'

     case(10)
        y=atan(tan(x))
        testline='y=atan(tan(x))'

     case(11)
        y=tan(atan(x))
        testline='y=tan(atan(x))'

     case(12)
        y=(-x)*(-1.0D0)
        testline='y=(-x)*(-1.0D0)'

     case default
        done=.true.

  end select
  if (.not.done) then 
     y=sin(y)
     dumpedTestLine=.false.
     ! test the value: 
     if (abs(y%v-xp)>myEps) then
       if (.not.dumpedTestLine) then 
         write(*,'(A,A)') 'deviation for ', testLine
         dumpedTestLine=.true.
       end if
       write(*,'(A,E25.17E3,A,E25.17E3,A,E22.14E3)')  '  y%v=',y%v,' x%v=',xp, ' diff: ', abs(y%v-xp)
       stop 1
     end if 
     ! test the coefficients
     do i=1,directions
       do j=1,order
        call RAget(y,i,j,yCoeff(i,j))
        if (abs(yCoeff(i,j)-xCoeff(i,j))>myEps) then
          if (.not.dumpedTestLine) then 
            write(*,'(A,A)') 'deviation for ', testLine
            dumpedTestLine=.true.
          end if
          write(*,'(A,I1,A,I2,A,E25.17E3,A,I1,A,I2,A,E25.17E3,A,E25.17E3)') '  y(',i,',',j,')=',&
yCoeff(i,j),' x(',i,',',j,')=',xCoeff(i,j), ' diff: ', abs(yCoeff(i,j)-xCoeff(i,j))
          stop 1
        end if
       end do
     end do
     if (.not.dumpedTestLine) then 
       write(*,'(A,A,A)') 'test ', testLine, ' ok'
     end if            
  end if
  testCase=testCase+1
  end do

end program 
