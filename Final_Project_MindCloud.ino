////// LIBRARIES ///////////////////////
#include <Servo.h>
#include <string.h>
/////////////////////// PINS ///////////////////////
//keypad 
int KEYPAD_PIN = PIN_PC0;
int keyIN = 0; //stores the keypad input

//servo
int servo_motor = PIN_PB1;
Servo servo; //creates a servo object

//motor
int motor = PIN_PC5;

//pir
int pir = PIN_PB0;

//temp sensor
int temp = PIN_PC1;

//rgb
int ledRGB[3] = {PIN_PB7,PIN_PB6,PIN_PB5};

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
      String old_password;
      Serial.println("Enter OLD password:");
      old_password = get_string();

      //if the entered password is the correect
      if (check_password(old_password)){
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
    bool check_password(String& input_password){
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
bool flag = 0;

/////////////////////// MAIN ///////////////////////
void setup(){
  Serial.begin(9600);
  //servo
  servo.attach(servo_motor); //links servo object with our servo motor(pin)
  
  //motor
  pinMode(motor, OUTPUT);

  //pir
  pinMode(pir, INPUT);

  //temp sensor
  pinMode(temp, INPUT);

  //rgb
  for (int i=0; i<3; i++){
    pinMode(ledRGB[i], OUTPUT);
  }

}

void loop(){
  //always read keys
  keyIN = analogRead(KEYPAD_PIN);
  String x = get_char(keyIN);
   

  //see if a key is pressed and save it
  if (x != ""){
    if (x == "#"){ 
      if (flag == 0){ //first time adding a password
        Serial.println("Enter your First password:");
        mypassword.set_initial_password (get_string());
        Serial.println("Password Saved!");
        flag = 1; //make sure that the flag is set 
      }
      else{ //not the first password but we are changing the password
        mypassword.change_password();
      }
    }
    else if (x == "*"){ //password tester
      mypassword.show_password();
    }
  }
   
}


