#include <SPI.h>
#include "Mirf.h"
#include "nRF24L01.h"
#include "MirfHardwareSpiDriver.h"

#define ID 39
#define GREEN_LED_PIN A4
#define RED_LED_PIN A5

enum MessageType : byte {
  CMD = 1,
  ACK = 2,
  NACK = 3,
  NONE = 4
};

struct ServoCommand {
  byte type;
  byte id;
  char joint[3];
  float angle;
  byte checksum;
};

enum TxState { TX_IDLE, TX_SENDING, TX_WAIT_ACK };

Nrf24l Mirf = Nrf24l(9, 10);
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

byte computeChecksum(byte* data, int length) {
  byte sum = 0;
  for (int k = 0; k < length; k++) sum ^= data[k];
  return sum;
}

void updateTxState()
{
  switch (txState) {
    case TX_IDLE:
      if (millis() - lastSendTime >= SEND_INTERVAL) {
        cmd.checksum = computeChecksum((byte*)&cmd, sizeof(cmd) - 1);
        Mirf.send((byte*)&cmd);
        txInProgress = true;
        txState = TX_SENDING;
        Serial.println("TX: Sent command");
        digitalWrite(GREEN_LED_PIN, HIGH);
        lastSendTime = millis();
      }
      break;

    case TX_SENDING:
      if (txInProgress && !Mirf.isSending()) {
        txInProgress = false;
        txStartTime = millis();
        txState = TX_WAIT_ACK;
        digitalWrite(GREEN_LED_PIN, LOW);
      }
      break;

    case TX_WAIT_ACK:
      if (Mirf.dataReady()) {
        Mirf.getData((byte*)&rxReply);
        if (rxReply.type == ACK && rxReply.id == cmd.id) {
          Serial.println("TX: ACK received");
          digitalWrite(GREEN_LED_PIN, HIGH);
          txState = TX_IDLE;
          retryCount = 0;
        } else {
          Serial.println("TX: NACK or wrong ID");
          digitalWrite(RED_LED_PIN, HIGH);
        }
      } else if (millis() - txStartTime > ACK_TIMEOUT) {
        retryCount++;
        if (retryCount < MAX_RETRIES) {
          Serial.println("TX: Retrying...");
          Mirf.send((byte*)&cmd);
          txInProgress = true;
          txState = TX_SENDING;
        } else {
          Serial.println("TX: Max retries reached");
          digitalWrite(RED_LED_PIN, HIGH);
          txState = TX_IDLE;
          retryCount = 0;
        }
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
  Mirf.setTADDR((byte *)"base");
  Mirf.setRADDR((byte *)"robot");
  Mirf.channel = 90;
  Mirf.payload = sizeof(ServoCommand);
  Mirf.config();
}

void loop() {
  updateTxState();
}
