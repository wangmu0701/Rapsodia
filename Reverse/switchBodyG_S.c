		

#ifdef ADDRESS_LOC
rev_ws=*(float*)rev_source;
*(float*)rev_source=0.0;
#endif
#ifdef INTEGER_LOC
#ifndef RA_ACC_ON_LOC
rev_ws=*(float*)loc_addr[(int)rev_source];
*(float*)loc_addr[(int)rev_source]=0.0;
#endif
#ifdef RA_ACC_ON_LOC
rev_ws=(float)loc_ad[(int)rev_source];
loc_ad[(int)rev_source]=0.0;
#endif
#endif

for(rev_i=0;rev_i<rev_nop;rev_i++){
  RA_NEXT_DOUBLE((&stackCursor),rev_vald)
  RA_NEXT_LOCATION((&stackCursor),rev_operand)
  RA_NEXT_INT((&stackCursor),rev_type)

  switch(rev_type){
    case floatS:
#ifdef ADDRESS_LOC
      *(float*)rev_operand+=(float)(rev_ws*rev_vald);
#endif
#ifdef INTEGER_LOC
#ifndef RA_ACC_ON_LOC
      *(float*)loc_addr[(int)rev_operand]+=(float)(rev_ws*rev_vald);
#endif
#ifdef RA_ACC_ON_LOC
      loc_ad[(int)rev_operand]+=rev_ws*rev_vald;
#endif
#endif
      break;
    case floatD:
#ifdef ADDRESS_LOC
      *(double*)rev_operand+=rev_ws*rev_vald;
#endif
#ifdef INTEGER_LOC
#ifndef RA_ACC_ON_LOC
      *(double*)loc_addr[(int)rev_operand]+=rev_ws*rev_vald;
#endif
#ifdef RA_ACC_ON_LOC
      loc_ad[(int)rev_operand]+=rev_ws*rev_vald;
#endif
#endif
      break;
    default:
      revInternalError(-5);
      break;
  }
}

