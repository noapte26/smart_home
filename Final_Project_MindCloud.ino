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
  423, 454, 503, 562,
  429, 459, 507, 565,
  451, 480, 525, 579,
  462, 487, 531, 585};

int range = 1; //tolerance

String get_char(int keyIN){
  String temp = ""; //empty string to store char
  for (int i=0; i<16; i++){
    //if the measured value of the pressed key is within range
    if (keyIN >= keysVAL[i]-range && keyIN <= keysVAL[i]+range){
      temp = keys[i];
    }
  }
  return temp;
}

class Password{
  public:
    String ans = "";

    void change_pass(){
      ans = "";
      String x = "";
      do{
        keyIN = analogRead(KEYPAD_PIN);
        x = get_char(keyIN);
        ans += x;
        x = ""; //empty the value in x
      } while (x != "#");
      
    }

    void check_pass(){
      String temp = "";
      String x = "";
      do{
        keyIN = analogRead(KEYPAD_PIN);
        x = get_char(keyIN);
        temp += x;
        x = ""; //empty the value in x
      } while (x != "#");

      if (ans == temp){
        //right password
      }
      else{
        //wrong password
      }
    }
};


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
  // Print if key pressed
  keyIN = analogRead(KEYPAD_PIN);
  Serial.println(get_char(keyIN));
  
}


