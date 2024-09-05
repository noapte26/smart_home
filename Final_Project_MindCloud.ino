////// LIBRARIES ///////////////////////
#include <Keypad.h>
#include <Servo.h>

/////////////////////// PINS ///////////////////////
//keypad 
//NOTE: if we will use SPI commu use PORTD, if we will use UART use PORTB
byte rowPins[4] = {PIN_PD0, PIN_PD1, PIN_PD2, PIN_PD3}; 
byte colPins[4] = {PIN_PD4, PIN_PD5, PIN_PD6, PIN_PD7}; 

//servo
int servo_motor = PIN_PB1;
Servo servo; //creates a servo object

//motor
int motor = PIN_PC5;

//pir
int pir = PIN_PB0;

//temp sensor
int temp = PIN_PC0;

//rgb
int ledR = PIN_PB7;
int ledG = PIN_PB6;
int ledB = PIN_PB5;

/////////////////////// FUNCTIONS ///////////////////////
//keypad buttons
char hexaKeys[4][4] = { 
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};
//connect the keypad library to our custom library
Keypad customKeypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 


/////////////////////// MAIN ///////////////////////
void setup(){
  //servo
  servo.attach(servo_motor); //links servo object with our servo motor(pin)
  
  //motor
  pinMode(motor, OUTPUT);

  //pir
  pinMode(pir, INPUT);

  //temp sensor
  pinMode(temp, INPUT);

  //rgb
  pinMode(ledR, OUTPUT);
  pinMode(ledG, OUTPUT);
  pinMode(ledB, OUTPUT);
}

void loop(){

}


