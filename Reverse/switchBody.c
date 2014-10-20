#define FIND_AND_ASSIGN_TAPE_D		RA_NEXT_DOUBLE((&stackCursor),rev_vald)        \
                                        RA_NEXT_LOCATION((&stackCursor),rev_operand)   \
					rev_type=floatD;				\
					rev_taploc=findTaploc(rev_operand,rev_type);	\
					tape[rev_taploc]+=rev_vald*rev_wd;			\

#define FIND_AND_ASSIGN_TAPE_S		RA_NEXT_DOUBLE((&stackCursor),rev_vald)        \
                                        RA_NEXT_LOCATION((&stackCursor),rev_operand)   \
					rev_type=floatS;				\
					rev_taploc=findTaploc(rev_operand,rev_type);	\
					tape[rev_taploc]+=rev_vald*rev_wd;			\

	
switch(rev_trcode){
  case const_s:
  case const_d:
    break;
  case unary_s_s:
  case unary_d_s:
    FIND_AND_ASSIGN_TAPE_S
    break;
  case unary_d_d:
  case unary_s_d:
    FIND_AND_ASSIGN_TAPE_D
    break;
  case binary_s_s_s:
  case binary_d_s_s:
    FIND_AND_ASSIGN_TAPE_S
    FIND_AND_ASSIGN_TAPE_S
    break;
  case binary_s_s_d:
  case binary_d_s_d:
    FIND_AND_ASSIGN_TAPE_S
    FIND_AND_ASSIGN_TAPE_D
    break;
  case binary_s_d_s:
  case binary_d_d_s:
    FIND_AND_ASSIGN_TAPE_D
    FIND_AND_ASSIGN_TAPE_S
    break;
  case binary_s_d_d:
  case binary_d_d_d:
    FIND_AND_ASSIGN_TAPE_D
    FIND_AND_ASSIGN_TAPE_D
    break;
  default:
    revInternalError(-4);
    break;
}
