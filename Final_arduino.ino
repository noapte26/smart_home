////// LIBRARIES ///////////////////////
#include <Servo.h>
#include <string.h>
/////////////////////// PINS ///////////////////////
//keypad 
int KEYPAD_PIN = PIN_PC3; ////////aaaaa
int keyIN = 0; //stores the keypad input


//Defining the pins
#define ldr          PIN_PC0    //Analog pin for LDR
#define temp         PIN_PC2    //Analog pin for temperature sensor
#define rgb_red      PIN_PD4    //PWM pin for red LED
#define rgb_green    PIN_PD5    //PWM pin for green LED
#define rgb_blue     PIN_PD6    //PWM pin for blue LED
#define motor_1      PIN_PB1    //Motor control pin 1 IN1
#define motor_2      PIN_PB2    //Motor control pin 2 IN2
#define motor_en     PIN_PC1    //motor enable
#define buzzer       PIN_PD2    //Pin for buzzer
#define pir          PIN_PB7    //Pin for PIR sensor
#define servo_motor  PIN_PB0    //Pin for servo motor
#define led          PIN_PD7    //Pin for led (light system)

Servo servo; //creates a servo object


/////////////////////// FUNCTIONS ///////////////////////
//keypad buttons
char keys[16] =  //keypad characters
  {'1', '2', '3', 'A',
   '4', '5', '6', 'B',
   '7', '8', '9', 'C',
   '*', '0', '#', 'D'};

int keysVAL [16] = { //keypad numerical values
  501, 522, 542, 560,
  399, 429, 456, 481,
  248, 294, 335, 371,
  0,    79, 146, 204};

int range = 9; //tolerance

String get_char(int keyIN){
  String chr = ""; //empty string to store char
  for (int i=0; i<16; i++){
    //if the measured value of the pressed key is within range
    if (keyIN >= keysVAL[i]-range && keyIN <= keysVAL[i]+range){
      chr = keys[i];
    }
  }
  delay(215);
  return chr;
}

String get_string(){
  String str = ""; //empty string to store string
  String x = ""; //empty string to store char
  while (1){
        keyIN = analogRead(KEYPAD_PIN);
        x = get_char(keyIN);

        if (x == "*"){
          Serial.println("");
          return str;
        }
          

        Serial.print(x);
        str += x;
      }
  return str;
}

class Password{
  private:
    String password;
  public:
    //create a construct to save our password
    Password (String placeholder){ //use "this->" because password is private
      this->password = placeholder;
    }

    //set first password
    void set_initial_password(const String& initial_password){
      this->password = initial_password;
    }

    //change password function
    void change_password(){
      //if the entered password is the correect
      if (check_password(get_string())){
        Serial.println("Correct Password");
        Serial.println("Enter NEW password:");
        this->password = get_string();
        Serial.println("New Password Saved!");
      }
      //else if it is wrong
      else{
        Serial.println("WRONG password");
      }
    }

    //password checker
    bool check_password(String input_password){
      Serial.println("Enter password:");
      return (input_password == this->password); //returns 1 if the entered password is the same as the original password
    }

    //password getter (for testing only!)
    void show_password(){
      Serial.println("----------------------------------");
      Serial.print("current password is ");
      Serial.println(this->password);
      Serial.println("----------------------------------");

    }
};

//place holder password to be global across all scopes
Password mypassword("");
//a flag to see if it is the first time we enter a password or if we are changing it
bool flagg = 0;



/////////////////////// MAIN ///////////////////////
void setup(){
  Serial.begin(9600);
  //servo
  servo.attach(servo_motor); //links servo object with our servo motor(pin)
  pinMode(servo_motor, OUTPUT);

  // Buzzer
  pinMode(buzzer, OUTPUT);

  // LED (lighting system)
  pinMode(led, OUTPUT);
  
  //motor
  pinMode(motor_1, OUTPUT);
  pinMode(motor_2, OUTPUT);

  //pir
  pinMode(pir, INPUT);

  //temp sensor
  pinMode(temp, INPUT);

  //rgb
  pinMode(rgb_red, OUTPUT);
  pinMode(rgb_green, OUTPUT);
  pinMode(rgb_blue, OUTPUT);
  //setting the initial state of RGB LED to off
  analogWrite(rgb_red, 0);
  analogWrite(rgb_green, 0);
  analogWrite(rgb_blue, 0);
  
}

void loop(){
  //always read keys
  keyIN = analogRead(KEYPAD_PIN);
  String x = get_char(keyIN);
   

  //see if a key is pressed and save it
  if (x != ""){
    if (x == "#"){ 
      if (flagg == 0){ //first time adding a password
        Serial.println("Enter your First password:");
        mypassword.set_initial_password (get_string());
        Serial.println("Password Saved!");
        flagg = 1; //make sure that the flag is set 
      }
      else{ //not the first password but we are changing the password
        mypassword.change_password();
      }
    }
    else if (x == "*"){ //password tester
      mypassword.show_password();
    }
  }

///////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////
  if (1){
  ////////first,LDR and light system level

  //Read the LDR value (0-1023)
  int ldrValue = analogRead(ldr);

  //Map the LDR value to a PWM range (0-255)
  int lightLevel = map(ldrValue,0,1023,0,255);

  //Set the light system brightness
  analogWrite(led, lightLevel);

  // Print the LDR value and light level to the serial monitor
  Serial.print("LDR Value: ");
  Serial.print(ldrValue);
  Serial.print("Light Level: ");
  Serial.println(lightLevel);

  //Delay
  delay(200);


  ////////second,temperature and the outputs depending on it

  //Read the temperature sensor value (0-1023)
  int tempValue = analogRead(temp);

  // Convert the sensor value to a temperature in Celsius
  int temperature = map(tempValue, 0, 308, 0, 150);

  //Print the temperature(just for debugging)
  Serial.print("Temperature: ");
  Serial.println(temperature);

  //Control RGB LED based on the temperature
  if (temperature > 30.0) {
    //Temperature > 30 degree celsius, turn on red LED
    analogWrite(rgb_red, 255);
    analogWrite(rgb_green, 0);
    analogWrite(rgb_blue, 0);
  } else if (temperature > 20.0) {
    //20 degree celsius < Temperature <= 30 degree celsius, turn on green LED
    analogWrite(rgb_red, 0);
    analogWrite(rgb_green, 255);
    analogWrite(rgb_blue, 0);
  } else {
    //Temperature <= 20 degree celsius, turn on blue LED
    analogWrite(rgb_red, 0);
    analogWrite(rgb_green, 0);
    analogWrite(rgb_blue, 255);
  }
  
  //Control motor speed based on temperature
  int motorSpeed = map(temperature,20,80,128,255); //Adjust according to temp sensor range
  Serial.println(motorSpeed);                      //above 128 is high 
  analogWrite(motor_en, motorSpeed);
  digitalWrite(motor_1, 1);
  digitalWrite(motor_2, 0); //To rotate in one direction (Fan)


  ////Unlocking the door
  servo.write(90); //Rotate the servo to 90 degrees to unlock the door
  delay(500); //Wait for 2 second to ensure the servo reaches the position

  
  }else{
    /////Now the wrong password is entered or no password has been entered, door is locked and flag is zero
    //////PIR sensor

    //Read the PIR sensor value
  int motionDetected = digitalRead(pir);

  //Print the PIR sensor status to the Serial Monitor
  if (motionDetected == HIGH) {
    Serial.println("Motion detected, someone is inside!");
  } else {
    Serial.println("No motion detected, home is empty.");
  }
  delay(1000);  //Delay


  /////Buzzer ringing for 500 milliseconds
  digitalWrite(buzzer, HIGH);  // Turn on the buzzer
  delay(500);                     // Wait for 500 milliseconds
  digitalWrite(buzzer, LOW);   // Turn off the buzzer
  delay(500);                    // Wait for 500 second the repeat
  

  ////Warning messages
  Serial.println("Wrong password, Alert!");
  }
}
