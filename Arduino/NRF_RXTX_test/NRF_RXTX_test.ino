#include <SPI.h>
#include "Mirf.h"
#include "nRF24L01.h"
#include "MirfHardwareSpiDriver.h"

#define ID 39
#define GREEN_LED_PIN A4
#define RED_LED_PIN A5

#define TX 1
#define RX 2

#define DEBUG_PRINT_STATEMENTS false

int mode = RX;

enum MessageType : byte 
{
  CMD = 1,
  ACK = 2,
  NACK = 3,
  NONE = 4
};

struct ServoCommand
{
  byte type;
  byte id;
  char joint[3];
  float angle;
  byte checksum;
};

enum TxState { TX_IDLE, TX_SENDING, TX_WAIT_ACK };
enum RxState { RX_IDLE, RX_RESPONDING };

Nrf24l Mirf = Nrf24l(9, 10);

// TX Command Variables
ServoCommand cmd = {CMD, ID, {'T','X','0'}, 123.4, 0};
ServoCommand rxReply;
TxState txState = TX_IDLE;

bool txInProgress = false;
unsigned long lastSendTime = 0;
const unsigned long SEND_INTERVAL = 10;

unsigned long txStartTime = 0;
const unsigned long ACK_TIMEOUT = 10;
int retryCount = 0;
const int MAX_RETRIES = 3;

// Rx Command Variables
ServoCommand rep = {CMD, ID, {'l', 'h', 'e'}, 110.0, 0};
ServoCommand received;
ServoCommand reply; // ACK packet for receiver
bool sendInProgress = false;
RxState rxState = RX_IDLE;

byte computeChecksum(byte* data, int length)
{
  byte sum = 0;
  for (int k = 0; k < length; k++) sum ^= data[k];
  return sum;
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

void sendSerialResponse(ServoCommand message)
{
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

ServoCommand listenSerial(void)
{
  if (Serial.available())
  {
    String command = Serial.readStringUntil('\n');
    command.trim();

    char com[50];
    command.toCharArray(com, 50);
    ServoCommand serial_cmd = parseCommand(com);

    sendSerialResponse(serial_cmd);
    return serial_cmd;
  }
}

void updateTxState()
{
  switch (txState) 
  {
    case TX_IDLE:
      if (millis() - lastSendTime >= SEND_INTERVAL) 
      {
        cmd = listenSerial();
        cmd.checksum = computeChecksum((byte*)&cmd, sizeof(cmd) - 1);
        Mirf.send((byte*)&cmd);
        txInProgress = true;
        txState = TX_SENDING;
        if(DEBUG_PRINT_STATEMENTS) Serial.println("TX: Sent command");
        digitalWrite(GREEN_LED_PIN, HIGH);
        lastSendTime = millis();
      }
      break;

    case TX_SENDING:
      if (txInProgress && !Mirf.isSending()) 
      {
        txInProgress = false;
        txStartTime = millis();
        txState = TX_WAIT_ACK;
        digitalWrite(GREEN_LED_PIN, LOW);
      }
      break;

    case TX_WAIT_ACK:
      if (Mirf.dataReady())
      {
        Mirf.getData((byte*)&rxReply);
        if (rxReply.type == ACK && rxReply.id == cmd.id) 
        {
          if(DEBUG_PRINT_STATEMENTS) Serial.println("TX: ACK received");
          digitalWrite(GREEN_LED_PIN, HIGH);
          digitalWrite(RED_LED_PIN, LOW);
          txState = TX_IDLE;
          retryCount = 0;
        } 
        else 
        {
          if(DEBUG_PRINT_STATEMENTS) Serial.println("TX: NACK or wrong ID");
          digitalWrite(RED_LED_PIN, HIGH);
        }
      } 
      else if (millis() - txStartTime > ACK_TIMEOUT) 
      {
        retryCount++;
        if (retryCount < MAX_RETRIES) 
        {
          if(DEBUG_PRINT_STATEMENTS) Serial.println("TX: Retrying...");
          Mirf.send((byte*)&cmd);
          txInProgress = true;
          txState = TX_SENDING;
        } 
        else 
        {
          if(DEBUG_PRINT_STATEMENTS) Serial.println("TX: Max retries reached");
          digitalWrite(RED_LED_PIN, HIGH);
          txState = TX_IDLE;
          retryCount = 0;
        }
      }
      break;
  }
}

void sendNRF(ServoCommand message)
{
  if (!sendInProgress) 
  {
    message.checksum = computeChecksum((byte*)&message, sizeof(message) - 1);
    Mirf.send((byte*)&message);
    sendInProgress = true;
  }

  if (sendInProgress && !Mirf.isSending()) 
  {
    sendInProgress = false;
    if(DEBUG_PRINT_STATEMENTS) Serial.println("NRF: Transmission complete");
  }
}

void sendSerial(ServoCommand message)
{
  // Prep message for echo back to python
  char joint_buf[4];
  memcpy(joint_buf, message.joint, 3);
  joint_buf[3] = '\0';  // Null-terminate safely

  char angle_buf[10];
  dtostrf(message.angle, 6, 2, angle_buf);  // width=6, precision=2

  Serial.print(joint_buf);
  Serial.println(angle_buf);  // Output: "lha 190.90"

}

void updateRxState()
{
  switch (rxState) 
  {
    case RX_IDLE:
      if (Mirf.dataReady()) 
      {
        Mirf.getData((byte*)&received);
        byte expected = computeChecksum((byte*)&received, sizeof(received) - 1);
        if(DEBUG_PRINT_STATEMENTS) Serial.println("RX: Packet received");

        if (expected == received.checksum) 
        {
          if(DEBUG_PRINT_STATEMENTS) 
          {
            Serial.print("RX: Joint ");
            Serial.print(received.joint[0]);
            Serial.print(received.joint[1]);
            Serial.print(received.joint[2]);
            Serial.print(" angle ");
            Serial.println(received.angle);
          }
          
          reply = {ACK, received.id, {'A', 'C', 'K'}, 0.0, 0};
          digitalWrite(GREEN_LED_PIN, HIGH);
        } 
        else 
        {
          reply = {NACK, received.id, {'N', 'A', 'K'}, 0.0, 0};
          if(DEBUG_PRINT_STATEMENTS) Serial.println("RX: Checksum mismatch");
          digitalWrite(RED_LED_PIN, HIGH);
        }

        sendNRF(reply);
        sendSerial(received); 
        rxState = RX_RESPONDING;
      }
      break;

    case RX_RESPONDING:
      sendNRF(reply);  // continue polling until done
      sendSerial(received); 
      if (!sendInProgress) 
      {
        rxState = RX_IDLE;
        digitalWrite(GREEN_LED_PIN, LOW);
      }
      break;
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);

  Mirf.spi = &MirfHardwareSpi;
  Mirf.init();
  if(mode == TX)
  {
    Mirf.setTADDR((byte *)"base");
    Mirf.setRADDR((byte *)"robot");
  }
  if(mode == RX)
  {
    Mirf.setTADDR((byte *)"robot");
    Mirf.setRADDR((byte *)"base");
  }
  Mirf.channel = 90;
  Mirf.payload = sizeof(ServoCommand);
  Mirf.config();
}

void loop() {
  if(mode == TX) updateTxState();
  if(mode == RX) updateRxState();
}
