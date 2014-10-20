int findTaploc(location operand, int type){
  for(rev_i=0;rev_i<tape_len;rev_i++){
    if (tape_key[rev_i]==operand){
      tape_type[rev_i]=type;
      return rev_i;
    }
  }
  if (tape_len>=MAX_LOCAL_TAPE){
    revInternalError(-3);
  }
  rev_i=tape_len++;
  tape_key[rev_i]=operand;
  tape[rev_i]=0.0;
  tape_type[rev_i]=type;
  return rev_i;
}
void pushTapeToGlobal(location source, int stype){
  rev_nop=0;
  for(rev_i=0;rev_i<tape_len;rev_i++){
    if (tape_type[rev_i]!=NULLType){
      rev_nop++;
//Questionable for Fortran
      RA_PUSH_INT((&gStack),tape_type[rev_i])
      RA_PUSH_LOCATION((&gStack),tape_key[rev_i])
      RA_PUSH_DOUBLE((&gStack),tape[rev_i])
    }
  }
  RA_PUSH_INT((&gStack),rev_nop)
  RA_PUSH_INT((&gStack),stype)
  RA_PUSH_LOCATION((&gStack),source)
}

int getSourceType(int trcode){
  int ret;
  switch(trcode){
    case const_s:
    case unary_s_s:
    case unary_s_d:
    case binary_s_s_s:
    case binary_s_s_d:
    case binary_s_d_s:
    case binary_s_d_d:
      ret=floatS;
      break;
    case const_d:
    case unary_d_s:
    case unary_d_d:
    case binary_d_s_s:
    case binary_d_s_d:
    case binary_d_d_s:
    case binary_d_d_d:
      ret=floatD;
      break;
    default:
      revInternalError(-4);
      break;
  }
  return ret;
}

void preAcc(){
  if (!revTraceOn) {return;}
  initCursorFromStack(&stackCursor,&lStack);
  rev_endflag=false;

  RA_NEXT_LOCATION((&stackCursor),rev_source)

  if (rev_source==NULLLOC){
    revInternalError(-1);
    return;
  }

  tape_len=1;
  tape[0]=1.0; //it must be!
  tape_key[0]=rev_source;

  RA_NEXT_INT((&stackCursor),rev_trcode)

  rev_stype=getSourceType(rev_trcode); 
  tape_type[0]=rev_stype;
  rev_staploc=0;
  rev_ttype=rev_stype;
  while(!rev_endflag){
    rev_wd=tape[rev_staploc];
    tape[rev_staploc]=0.0;
    tape_type[rev_staploc]=NULLType;
    #include "switchBody.c"
    popLocalStackToCursor(&lStack,&stackCursor);

    RA_NEXT_LOCATION((&stackCursor),rev_source);

    while((rev_source!=NULLLOC)&&(inActiveSource(rev_source))){

      RA_NEXT_INT((&stackCursor),rev_trcode)

      switch(rev_trcode){
        case const_s:
        case const_d:
          break;
        case unary_s_s:
        case unary_s_d:
        case unary_d_s:
        case unary_d_d:
          RA_NEXT_DOUBLE((&stackCursor),rev_vald)
          RA_NEXT_LOCATION((&stackCursor),rev_operand)
          break;
        case binary_s_s_s:
        case binary_s_s_d:
        case binary_s_d_s:
        case binary_s_d_d:
        case binary_d_s_s:
        case binary_d_s_d:
        case binary_d_d_s:
        case binary_d_d_d:
          RA_NEXT_DOUBLE((&stackCursor),rev_vald)
          RA_NEXT_LOCATION((&stackCursor),rev_operand)
          RA_NEXT_DOUBLE((&stackCursor),rev_vald)
          RA_NEXT_LOCATION((&stackCursor),rev_operand)
          break;
        default:
          revInternalError(-2);
          break;
      }
      RA_NEXT_LOCATION((&stackCursor),rev_source)
    }

    if (rev_source==NULLLOC){
      rev_endflag=true;
    }
    else{
      RA_NEXT_INT((&stackCursor),rev_trcode)
      rev_stype=getSourceType(rev_trcode); 
      rev_staploc=findTaploc(rev_source,rev_stype);
    }
  }
  pushTapeToGlobal(tape_key[0],rev_ttype);   
}

void eliminateBody(){
  rev_endflag=false;

  initCursorFromStack(&stackCursor,&lStack);

  while(!rev_endflag){
    RA_NEXT_LOCATION((&stackCursor),rev_source)
    while((rev_source!=NULLLOC)&&(inActiveSource(rev_source))){
      RA_NEXT_INT((&stackCursor),rev_trcode)
      switch(rev_trcode){
        case const_s:
        case const_d:
          break;
        case unary_s_s:
        case unary_s_d:
        case unary_d_s:
        case unary_d_d:
          RA_NEXT_DOUBLE((&stackCursor),rev_vald)
          RA_NEXT_LOCATION((&stackCursor),rev_operand)
          break;
        case binary_s_s_s:
        case binary_s_s_d:
        case binary_s_d_s:
        case binary_s_d_d:
        case binary_d_s_s:
        case binary_d_s_d:
        case binary_d_d_s:
        case binary_d_d_d:
          RA_NEXT_DOUBLE((&stackCursor),rev_vald)
          RA_NEXT_LOCATION((&stackCursor),rev_operand)
          RA_NEXT_DOUBLE((&stackCursor),rev_vald)
          RA_NEXT_LOCATION((&stackCursor),rev_operand)
          break;
        default:
          revInternalError(-2);
          break;
      }
      RA_NEXT_LOCATION((&stackCursor),rev_source)
    }
    if (rev_source==NULLLOC){
      rev_endflag=true;
    }
    else{
      RA_NEXT_INT((&stackCursor),rev_trcode)
      rev_stype=getSourceType(rev_trcode); 
      rev_staploc=findTaploc(rev_source,rev_stype);
      rev_wd=tape[rev_staploc];
      tape[rev_staploc]=0.0;
      tape_type[rev_staploc]=NULLType;
      #include "switchBody.c"
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

  tape_len=0;
  while(!rev_endflag){
    RA_NEXT_INT((&stackCursor),rev_stype);
    RA_NEXT_INT((&stackCursor),rev_nop);
    switch(rev_stype){
      case floatS:
        #include"switchBodyG_S.c"
        break;
      case floatD:
        #include"switchBodyG_D.c"
        break;
      default:
        revInternalError(-5);
        break;
    }
    RA_NEXT_LOCATION((&stackCursor),rev_source)
    if (rev_source==(location)NULLLOC) {
      rev_endflag=true;
    }
  }
}
