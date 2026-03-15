#include <Adafruit_LiquidCrystal.h>

Adafruit_LiquidCrystal lcd_1(0);

// Button pins
const int btn1 = 2;
const int btn2 = 4;
const int btn3 = 6;

// LED pins
const int led1 = 8;
const int led2 = 10;
const int led3 = 12;

bool lastBtn1 = HIGH;
bool lastBtn2 = HIGH;
bool lastBtn3 = HIGH;

bool systemEnabled = false;   // 🔐 Control flag

void setup()
{
  Serial.begin(9600);

  pinMode(btn1, INPUT_PULLUP);
  pinMode(btn2, INPUT_PULLUP);
  pinMode(btn3, INPUT_PULLUP);

  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);

  // LEDs OFF (Active LOW setup)
  digitalWrite(led1, HIGH);
  digitalWrite(led2, HIGH);
  digitalWrite(led3, HIGH);
  
  lcd_1.begin(16, 2);
  lcd_1.setBacklight(1);
  lcd_1.setCursor(0,0);
  lcd_1.print("E - Secure");
  lcd_1.setCursor(0,1);
  lcd_1.print("Voting System");
  delay(1000);
  
  digitalWrite(led1, LOW);
  digitalWrite(led2, LOW);
  digitalWrite(led3, LOW);

  lcd_1.clear();
  lcd_1.print("Waiting for X");
}

void loop() {

  // 🔵 Check Serial for activation
  if (Serial.available()) {
    char cmd = Serial.read();
    if (cmd == 'x') {
      systemEnabled = true;
      lcd_1.clear();
      lcd_1.setCursor(0,0);
      lcd_1.print("DMK   TVK   ADMK");
    }
  }
  if (!systemEnabled) return;

  bool currentBtn1 = digitalRead(btn1);
  bool currentBtn2 = digitalRead(btn2);
  bool currentBtn3 = digitalRead(btn3);

  // ---------------- BUTTON 1 ----------------
  if (currentBtn1 == LOW) {
    digitalWrite(led1, LOW);
  } else {
    digitalWrite(led1, HIGH);
  }

  if (lastBtn1 == LOW && currentBtn1 == HIGH) {
    Serial.write('a');
    systemEnabled = false;   // disable after vote
    showResult("DMK");
  }

  // ---------------- BUTTON 2 ----------------
  if (currentBtn2 == LOW) {
    digitalWrite(led2, LOW);
  } else {
    digitalWrite(led2, HIGH);
  }

  if (lastBtn2 == LOW && currentBtn2 == HIGH) {
    Serial.write('b');
    systemEnabled = false;
    showResult("TVK");
  }

  // ---------------- BUTTON 3 ----------------
  if (currentBtn3 == LOW) {
    digitalWrite(led3, LOW);
  } else {
    digitalWrite(led3, HIGH);
  }

  if (lastBtn3 == LOW && currentBtn3 == HIGH) {
    Serial.write('c');
    systemEnabled = false;
    showResult("ADMK");
  }

  lastBtn1 = currentBtn1;
  lastBtn2 = currentBtn2;
  lastBtn3 = currentBtn3;

  delay(10);
}

// 🔹 Function to show result and reset display
void showResult(String party) {
  lcd_1.clear();
  lcd_1.setCursor(6,0);
  lcd_1.print(party);
  lcd_1.setCursor(0,1);
  lcd_1.print("Voting Completed");

  delay(2000);

  // Turn OFF LEDs after vote
  digitalWrite(led1, LOW);
  digitalWrite(led2, LOW);
  digitalWrite(led3, LOW);

  lcd_1.clear();
  lcd_1.print("Waiting...");
}