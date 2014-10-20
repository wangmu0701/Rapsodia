
void pushTapeToGlobal(location source){
  rev_nop=0;
  for(rev_i=0;rev_i<tape_len;rev_i++){
    if (tape[rev_i]!=0.0){
      rev_nop++;
      RA_PUSH_LOCATION((&gStack),tape_key[rev_i])
      RA_PUSH_DOUBLE((&gStack),tape[rev_i])
    }
  }
  RA_PUSH_INT((&gStack),rev_nop)
  RA_PUSH_LOCATION((&gStack),source)
}
int findTapLoc(location operand) {
  for(rev_i=0;rev_i<tape_len;rev_i++){
    if (tape_key[rev_i]==operand){
      return rev_i;
    }
  }
  if (tape_len>=MAX_LOCAL_TAPE){
    revInternalError(-3);
  }
  tape_key[rev_i]=operand;
  tape[rev_i]=0.0;
  tape_len++;
  return rev_i;  
}
void preAcc(){
  if (!revTraceOn) {return;}
  initCursorFromStack(&stackCursor,&lStack);
  rev_endflag=false;

  RA_NEXT_LOCATION((&stackCursor),rev_source)

  tape[0]=1.0; //it must be!
  tape_key[0]=rev_source;
  tape_type[0]=floatD;
  tape_len=1;
  while(!rev_endflag){
    rev_staploc=findTapLoc(rev_source);
    rev_wd=tape[rev_staploc];
    tape[rev_staploc]=0.0;
    tape_type[rev_staploc]=NULLType;
    RA_NEXT_INT((&stackCursor),rev_nop)

    switch (rev_nop) {
      case 2:
        RA_NEXT_DOUBLE((&stackCursor),rev_vald)
        RA_NEXT_LOCATION((&stackCursor),rev_operand)
        rev_taploc=findTapLoc(rev_operand);
        tape[rev_taploc]+=rev_wd*rev_vald;tape_type[rev_taploc]=floatD;
      case 1:
        RA_NEXT_DOUBLE((&stackCursor),rev_vald)
        RA_NEXT_LOCATION((&stackCursor),rev_operand)
        rev_taploc=findTapLoc(rev_operand);
        tape[rev_taploc]+=rev_wd*rev_vald;tape_type[rev_taploc]=floatD;
        break;
      default:
        revInternalError(-2);
    }
    popLocalStackToCursor(&lStack,&stackCursor);

    RA_NEXT_LOCATION((&stackCursor),rev_source)

    while((rev_source!=(location)NULLLOC)&&(inActiveSource(rev_source))){
      RA_NEXT_INT((&stackCursor),rev_nop)
      switch (rev_nop) {
        case 2:
          RA_NEXT_DOUBLE((&stackCursor),rev_vald)
          RA_NEXT_LOCATION((&stackCursor),rev_operand)
        case 1:
          RA_NEXT_DOUBLE((&stackCursor),rev_vald);
          RA_NEXT_LOCATION((&stackCursor),rev_operand)
          break;
        default:
          revInternalError(-2);
      }

      RA_NEXT_LOCATION((&stackCursor),rev_source)

    }
    if (rev_source==(location)NULLLOC){
      rev_endflag=true;
    }
  }
  pushTapeToGlobal(tape_key[0]);    
}

void eliminateBody(){
  rev_endflag=false;

  initCursorFromStack(&stackCursor,&lStack);

  while(!rev_endflag){
    RA_NEXT_LOCATION((&stackCursor),rev_source)
    while((rev_source!=NULLLOC)&&(inActiveSource(rev_source))){
      RA_NEXT_INT((&stackCursor),rev_nop)
      switch (rev_nop) {
        case 2:
          RA_NEXT_DOUBLE((&stackCursor),rev_vald)
          RA_NEXT_LOCATION((&stackCursor),rev_operand)
        case 1:
          RA_NEXT_DOUBLE((&stackCursor),rev_vald)
          RA_NEXT_LOCATION((&stackCursor),rev_operand)
          break;
        default:
          revInternalError(-2);
      }
      RA_NEXT_LOCATION((&stackCursor),rev_source)
    }
    if (rev_source==NULLLOC){
      rev_endflag=true;
    }
    else{
      RA_NEXT_INT((&stackCursor),rev_nop)
      rev_staploc=findTapLoc(rev_source);
      rev_wd=tape[rev_staploc];
      tape[rev_staploc]=0.0;
      tape_type[rev_staploc]=NULLType;
      switch (rev_nop) {
        case 2:
          RA_NEXT_DOUBLE((&stackCursor),rev_vald)
          RA_NEXT_LOCATION((&stackCursor),rev_operand)
          rev_taploc=findTapLoc(rev_operand);
          tape[rev_taploc]=1.0;tape_type[rev_taploc]=floatD;
        case 1:
          RA_NEXT_DOUBLE((&stackCursor),rev_vald)
          RA_NEXT_LOCATION((&stackCursor),rev_operand)
          rev_taploc=findTapLoc(rev_operand);
          tape[rev_taploc]=1.0;tape_type[rev_taploc]=floatD;
          break;
        default:
          revInternalError(-2);
      }
      popLocalStackToCursor(&lStack,&stackCursor);
    }
  }
}



void eliminateResiduals(location a, location b){
  tape[0]=1.0;tape_key[0]=a;tape_type[0]=floatD;
  tape[1]=1.0;tape_key[1]=b;tape_type[1]=floatD;
  tape_len=2;
  eliminateBody();
}
void eliminateResidual(location a){
  tape[0]=1.0;tape_key[0]=a;tape_type[0]=floatD;
  tape_len=1;
  eliminateBody();
}


//flat design, no stack variables
void reduction(){        
  stackCursor.cur_blk=gStack.cur_blk;
  stackCursor.curr_len=gStack.cur_blk->curr_len;
  stackCursor.avlb_len=gStack.cur_blk->avlb_len;

  rev_endflag=false;

  RA_NEXT_LOCATION((&stackCursor),rev_source)

  while(!rev_endflag){
#ifdef ADDRESS_LOC
    rev_wd=*(double*)rev_source;
    *(double*)rev_source=0.0;
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
    RA_NEXT_INT((&stackCursor),rev_nop);

    for(rev_i=0;rev_i<rev_nop;rev_i++){
      RA_NEXT_DOUBLE((&stackCursor),rev_vald)

      RA_NEXT_LOCATION((&stackCursor),rev_operand)

#ifdef ADDRESS_LOC
      *(double*)rev_operand+=rev_wd*rev_vald;
#endif
#ifdef INTEGER_LOC
#ifndef RA_ACC_ON_LOC
      *(double*)loc_addr[(int)rev_operand]+=rev_wd*rev_vald;
#endif
#ifdef RA_ACC_ON_LOC
      loc_ad[(int)rev_operand]+=rev_wd*rev_vald;
#endif
#endif
    }

    RA_NEXT_LOCATION((&stackCursor),rev_source)

  }
}
