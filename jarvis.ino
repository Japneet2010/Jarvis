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
