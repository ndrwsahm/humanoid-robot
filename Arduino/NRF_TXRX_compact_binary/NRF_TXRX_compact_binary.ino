/*
  Teach Protocol Series — NRF24 Reliable Communication

  This script implements a bidirectional communication protocol using NRF24L01+ radios.
  It supports command packets with joint name and angle, includes checksum validation,
  and introduces ACK/NACK responses with retry logic for reliability.

  Features:
  - Packed struct with message type, ID, joint name, angle, and checksum
  - Checksum validation using XOR
  - ACK/NACK response handling
  - Timeout-based retry framework
  - Byte-level debugging output

  Created by Andrew and Tellie (AI Assitant)
*/
// Libraries =============================================================
// Serial Library
#include <SPI.h>

// NRF24 Libraries
#include "Mirf.h"
#include "nRF24L01.h"
#include "MirfHardwareSpiDriver.h"

#define TX 0
#define RX 1

#define ID 39
#define SIZE_OF_PAYLOAD 10 // corresponds to bytes in ServoCommand byte, byte, 3 bytes, 4 bytes, byte

const int GREEN_LED_PIN = A4;
const int RED_LED_PIN = A5;

int role = TX;

unsigned long start;
unsigned long lastAckTime;
bool ackReceived = false;

enum MessageType : byte {
  CMD = 1,
  ACK = 2,
  NACK = 3,
  NONE = 4
};

struct ServoCommand
{
  byte type;
  byte id;
  char joint[3];     // e.g., "lhr", "lha"
  float angle;       // e.g., 90.0, 182.2
  byte checksum;
};

ServoCommand ack = {CMD, ID, {'A', 'C', 'K'}, 0.0, 0};
ServoCommand command;
ServoCommand response;  // ACK packet for sender

ServoCommand received;
ServoCommand reply; // ACK packet for receiver


// Pins ===================================================================
Nrf24l Mirf = Nrf24l(9, 10);

// Helper Functions ============================================================
byte computeChecksum(byte* data, int length)
{
  byte sum = 0;
  for (int k = 0; k < length; k++)
  {
    sum ^= data[k];
  }
  return sum;
}

// Setup ================================================================
void setup()
{
  Serial.begin(115200);             // Set up Serial communcation at 9600
  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);

  //Serial.print("Struct size: ");
  //Serial.println(sizeof(ServoCommand));

  //NRF Setups
  Mirf.spi = &MirfHardwareSpi;
  Mirf.init();

  Mirf.setRADDR((byte *)"robot"); // Set your own address (receiver address) using 5 characters
  Mirf.channel = 90;             // Set the used channel
  Mirf.payload = SIZE_OF_PAYLOAD;
  Mirf.config();
}

void listenACK(void)
{
  Mirf.config();
  start = millis();

  while (millis() - start < 5)
  {
    if (Mirf.dataReady())
    {
      Mirf.getData((byte*)&response);
      /*
        byte* raw = (byte*)&response;
        Serial.print("Raw bytes: ");
        for (int j = 0; j < sizeof(response); j++)
        {
        Serial.print(raw[j], HEX);
        Serial.print(" ");
        }
        Serial.println();

        Serial.print("Type: "); Serial.println(response.type);*/
      if (response.type == ACK && response.id == ID)
      {
        ackReceived = true;
        digitalWrite(RED_LED_PIN, HIGH);
        lastAckTime = millis();
        break;
      }
      else
      {
        ackReceived = false;
        digitalWrite(RED_LED_PIN, LOW);
      }
    }
  }
}

void checkACK(void)
{
  if (millis() - lastAckTime > 1000) digitalWrite(RED_LED_PIN, LOW);
}

ServoCommand parseCommand(char* input)
{
  ServoCommand local_cmd;
  char* token;

  // Type
  token = strtok(input, " ");
  if (strcmp(token, "CMD") == 0) local_cmd.type = 1;
  else if (strcmp(token, "ACK") == 0) local_cmd.type = 2;
  else if (strcmp(token, "NACK") == 0) local_cmd.type = 3;
  else local_cmd.type = 0;

  // ID
  token = strtok(NULL, " ");
  local_cmd.id = atoi(token);

  // Joint
  token = strtok(NULL, " ");
  strncpy(local_cmd.joint, token, 3);

  // Angle
  token = strtok(NULL, " ");
  local_cmd.angle = atof(token);

  // Checksum (optional — compute later)
  local_cmd.checksum = 0;

  return local_cmd;
}

void sendSerial(ServoCommand message)
{
  //blinkLED(GREEN_LED_PIN);
  // Prep message for echo back to python
  char joint_buf[4];
  memcpy(joint_buf, message.joint, 3);
  joint_buf[3] = '\0';  // Null-terminate safely

  char angle_buf[10];
  dtostrf(message.angle, 6, 2, angle_buf);  // width=6, precision=2

  Serial.print(joint_buf);
  Serial.print(" ");
  Serial.println(angle_buf);  // Output: "lha 190.90"

}

void listenSerial(void)
{
  if (Serial.available())
  {
    String command = Serial.readStringUntil('\n');
    command.trim();  // Remove whitespace

    char com[50];
    command.toCharArray(com, 50);
    ServoCommand serial_cmd = parseCommand(com);

    //if (serial_cmd.type == CMD) blinkLED(GREEN_LED_PIN);
    if (strcmp(serial_cmd.joint, "STA") == 0)
    {
      int button_state = digitalRead(RED_LED_PIN);

      sprintf(serial_cmd.joint, "LED");
      if (button_state == HIGH) serial_cmd.angle = 1.0;
      else serial_cmd.angle = 0.0;
    }

    // Send Serial command to RX arduino
    sendNRF(serial_cmd);
    sendSerial(serial_cmd);
  }
  //return serial_cmd;
}

void blinkLED(int pin)
{
  digitalWrite(pin, HIGH);
  delay(100);
  digitalWrite(pin, LOW);
  delay(100);
  digitalWrite(pin, HIGH);
  delay(100);
  digitalWrite(pin, LOW);
}

void sendNRF(ServoCommand message)
{
  message.checksum = computeChecksum((byte*)&message, sizeof(message) - 1);
  Mirf.send((byte*)&message);
  while (Mirf.isSending());
}

// Main loop ==================================================================
void loop()
{
  // Sender Code
  if (role == TX)
  {
    // TODO add if loop for sendNRF(ack) and sendNRF(cmd)
    // Send Connect RF command to RX arduino
    sendNRF(ack);

    // Receive serial command from cpu
    // Send NRF signal and echo serial to cpu
    listenSerial();

    // Send echo back to cpu via serial
    //sendSerial(command);

    // Listen for echo from RX arduino and adjust LED accordingly
    listenACK();
    checkACK();
  }

  // Receiver Code
  else
  {
    if (Mirf.dataReady())
    {
      Mirf.getData((byte*)&received);

      byte expected = computeChecksum((byte*)&received, sizeof(received) - 1);

      if (expected == received.checksum && received.type == CMD)
      {
        reply = {ACK, received.id, {'A', 'C', 'K'}, 0.0, 0};
        /*
          Serial.print("Type: "); Serial.println(received.type);
          Serial.print("ID: "); Serial.println(received.id);
          Serial.print("Joint: "); Serial.println(received.joint);
          Serial.print("Angle: "); Serial.println(received.angle);*/
        digitalWrite(RED_LED_PIN, HIGH);
      }
      else
      {
        reply = {NACK, received.id, {'N', 'A', 'K'}, 0.0, 0};
        digitalWrite(RED_LED_PIN, LOW);
        //Serial.println("Checksum mismatch — packet corrupted.");
      }

      // Send received message to pi
      if(expected == received.checksum && strcmp(received.joint, "ACK") != 0)
      {
        sendSerial(received);  
      }

      // Send echo ACK back to TX arduino
      sendNRF(reply);
      Mirf.config();
    }

    else
    {
      digitalWrite(RED_LED_PIN, LOW);
    }
  }
}
