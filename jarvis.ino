int ledPin = 7;  // LED connected to digital pin 7
int receivedData = 0;  // Variable to store received data

void setup() {
  pinMode(ledPin, OUTPUT);  // Set pin 7 as output
  Serial.begin(9600);  // Start serial communication at 9600 baud
}

void loop() {
  // Check if data is available to read from the serial port
  if (Serial.available() > 0) {
    receivedData = Serial.read();  // Read the incoming data

    // Switch ON the LED if data received is '1'
    if (receivedData == '1') {
      digitalWrite(ledPin, HIGH);  // Turn the LED on
    } 
    // Switch OFF the LED if data received is '0'
    else if (receivedData == '0') {
      digitalWrite(ledPin, LOW);  // Turn the LED off
    }
  }
}
//
//#include <Servo.h>
//
//Servo myServo;
//int ledPin = 7;
//int servoPin = 8;
//int meanPos = 90;  // Define the mean position of the servo motor
//
//void setup() {
//  Serial.begin(9600);
//  myServo.attach(servoPin);
//  pinMode(ledPin, OUTPUT);
//  myServo.write(meanPos);  // Start at the mean position
//}
//
//void loop() {
//  if (Serial.available()) {
//    char command = Serial.read();
//
//    // LED Control
//    if (command == '1') {
//      digitalWrite(ledPin, HIGH);  // Turn on LED
//    } else if (command == '0') {
//      digitalWrite(ledPin, LOW);   // Turn off LED
//    }
//
//    // Servo Control
//    if (command == 'R') {
//      myServo.write(meanPos + 90);  // Turn right (90 degrees clockwise)
//    } else if (command == 'L') {
//      myServo.write(meanPos - 90);  // Turn left (90 degrees counterclockwise)
//    } else if (command == 'M') {
//      myServo.write(meanPos);  // Move back to the mean position
//    }
//  }
//}
//
//
