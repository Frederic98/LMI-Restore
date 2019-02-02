void homeSwitch(){
  if (!Homing_status){
    state = 4;
  }
}

void limitSwitch(){
  state = 4;
}

