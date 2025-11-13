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

int role = RX;

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

enum TxState 
{
  TX_IDLE, 
  TX_SENDING,
  TX_WAIT_ACK
};

enum RxState
{
  RX_IDLE,
  RX_RECEIVED,
  RX_RESPONDING
};

TxState txState = TX_IDLE;
ServoCommand txBuffer;
unsigned long txStartTime = 0;
const unsigned long ACK_TIMEOUT = 10;
int retryCount = 0;
const int MAX_RETRIES = 3;

RxState rxState = RX_IDLE;
unsigned long rxStartTime = 0;
const unsigned long RX_RESPONSE_DELAY = 0;

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

void startTx(ServoCommand msg)
{
  txBuffer = msg;
  txBuffer.checksum = computeChecksum((byte*)&txBuffer, sizeof(txBuffer) - 1);
  Mirf.send((byte*)&txBuffer);
  txState = TX_SENDING;
}

void updateTxState()
{
  switch(txState)
  {
    case TX_IDLE:
      break;
      
    case TX_SENDING:
      if(!Mirf.isSending())
      {
        txStartTime = millis();
        txState = TX_WAIT_ACK;
      }
      break;

    case TX_WAIT_ACK:
      if(Mirf.dataReady())
      {
        Mirf.getData((byte*)&response);
        if(response.type == ACK && response.id == ID)
        {
          ackReceived = true;
          digitalWrite(RED_LED_PIN, HIGH);
          lastAckTime = millis();
          txState = TX_IDLE;
          retryCount = 0;
        }
        else
        {
          ackReceived = false;
          digitalWrite(RED_LED_PIN, LOW);
        }
      }
      else if (millis() - txStartTime > ACK_TIMEOUT)
      {
        retryCount++;
        if(retryCount < MAX_RETRIES)
        {
          Mirf.send((byte*)&txBuffer);
          txState = TX_SENDING;
        }
      }
      else
      {
        txState = TX_IDLE;
        retryCount = 0;
      }
      break;
  }
}

void updateRxState()
{
  switch (rxState)
  {
    case RX_IDLE:
      if(Mirf.dataReady())
      {
        Mirf.getData((byte*)&received);
        rxState = RX_RECEIVED;
      }
      break;

    case RX_RECEIVED: 
    {
      byte expected = computeChecksum((byte*)&received, sizeof(received) - 1);

      if (expected == received.checksum && received.type == CMD) {
        reply = {ACK, received.id, {'A', 'C', 'K'}, 0.0, 0};
        digitalWrite(RED_LED_PIN, HIGH);
      } else {
        reply = {NACK, received.id, {'N', 'A', 'K'}, 0.0, 0};
        digitalWrite(RED_LED_PIN, LOW);
      }

      if (expected == received.checksum && strcmp(received.joint, "ACK") != 0) {
        sendSerial(received);
      }

      rxStartTime = millis();
      rxState = RX_RESPONDING;
      break;
    }
     case RX_RESPONDING:
      if (millis() - rxStartTime >= RX_RESPONSE_DELAY) {
        sendNRFReply(reply);
        rxState = RX_IDLE;
      }
      break;
  }
}

bool replyInProgress = false;

void sendNRFReply(ServoCommand message) {
  if (!replyInProgress) {
    message.checksum = computeChecksum((byte*)&message, sizeof(message) - 1);
    Mirf.send((byte*)&message);
    replyInProgress = true;
  }

  if (replyInProgress && !Mirf.isSending()) {
    replyInProgress = false;
  }
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

  if (role == TX)
  {
    Mirf.setTADDR((byte *)"base"); // Set your own address (receiver address) using 5 characters
    Mirf.setRADDR((byte *)"robot");
  }

  else
  {
    Mirf.setTADDR((byte *)"robot"); // Set your own address (receiver address) using 5 characters
    Mirf.setRADDR((byte *)"base");
  }
  Mirf.channel = 90;             // Set the used channel
  Mirf.payload = SIZE_OF_PAYLOAD;
  Mirf.config();
}

void listenACK(void)
{
  Mirf.config();
  start = millis();

  // TODO may need to thread this to make it smoother
  while (millis() - start < 5) // Blocking function of 5ms!!!!
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
    sendSerial(serial_cmd);
    startTx(serial_cmd);
  }
  //return serial_cmd;
}

// Main loop ==================================================================
void loop()
{
  // Sender Code
  if (role == TX)
  {
    if(txState == TX_IDLE) listenSerial();
    updateTxState();
    checkACK();
  }

  if (role == RX)
  {
    updateRxState();
  }
}
