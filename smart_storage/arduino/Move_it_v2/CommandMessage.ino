void CommandMessage() {

  if (Serial.available() > 3) {
    // read the incoming byte:
    StartChar = Serial.read();
    Row = Serial.read();
    column = Serial.read();
    EndChar = Serial.read();

    Serial.println(StartChar);
    Serial.println(Row);
    Serial.println(column);
    Serial.println(EndChar);

    if (StartChar == 'G' && EndChar == 'X') { // Check if StartChar is G for get
      state = 2;//Change the status to the get status


    }
    else if (StartChar == 'P' && EndChar == 'X') {
      state = 3; //Change status to the place status

    }
    else {
      Serial.println("Error");
    }


  }
}

