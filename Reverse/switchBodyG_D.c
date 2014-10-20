		

#ifdef ADDRESS_LOC
rev_wd=*(double*)rev_source;
*(double*)rev_source=0.0;
//printf("rev_source=<%lx>,rev_wd=<%10.5f>\n",(unsigned long)rev_source,rev_wd);
#endif
#ifdef INTEGER_LOC
#ifndef RA_ACC_ON_LOC
rev_wd=*(double*)loc_addr[(int)rev_source];
*(double*)loc_addr[(int)rev_source]=0.0;
#endif
#ifdef RA_ACC_ON_LOC
rev_wd=loc_ad[(int)rev_source];
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
      *(float*)rev_operand+=(float)(rev_wd*rev_vald);
#endif
#ifdef INTEGER_LOC
#ifndef RA_ACC_ON_LOC
      *(float*)loc_addr[(int)rev_operand]+=(float)(rev_wd*rev_vald);
#endif
#ifdef RA_ACC_ON_LOC
      loc_ad[(int)rev_operand]+=rev_wd*rev_vald;
#endif
#endif
      break;
    case floatD:
#ifdef ADDRESS_LOC
      *(double*)rev_operand+=rev_wd*rev_vald;
//printf("rev_operand=<%lx>,rev_vald=<%10.5f>,after=<%10.5f>\n",(unsigned long)rev_operand,rev_vald,*(double*)rev_operand);
#endif
#ifdef INTEGER_LOC
#ifndef RA_ACC_ON_LOC
      *(double*)loc_addr[(int)rev_operand]+=rev_wd*rev_vald;
#endif
#ifdef RA_ACC_ON_LOC
      loc_ad[(int)rev_operand]+=rev_wd*rev_vald;
#endif
#endif
      break;
    default:
      revInternalError(-5);
      break;
  }
}

