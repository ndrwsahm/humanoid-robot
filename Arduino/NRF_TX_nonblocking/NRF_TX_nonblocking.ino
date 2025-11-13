#include <SPI.h>
#include "Mirf.h"
#include "nRF24L01.h"
#include "MirfHardwareSpiDriver.h"

#define GREEN_LED_PIN A4
#define RED_LED_PIN A5

struct ServoCommand {
  byte type;
  byte id;
  char joint[3];
  float angle;
  byte checksum;
};

enum TxState { TX_IDLE, TX_SENDING, TX_WAIT_ACK };
TxState txState = TX_IDLE;
ServoCommand txBuffer;
unsigned long txStartTime = 0;
const unsigned long ACK_TIMEOUT = 10;
int retryCount = 0;
const int MAX_RETRIES = 3;

Nrf24l Mirf = Nrf24l(9, 10);
ServoCommand received;

byte computeChecksum(byte* data, int length) {
  byte sum = 0;
  for (int k = 0; k < length; k++) sum ^= data[k];
  return sum;
}

void startTx(ServoCommand msg) {
  txBuffer = msg;
  txBuffer.checksum = computeChecksum((byte*)&txBuffer, sizeof(txBuffer) - 1);
  Mirf.send((byte*)&txBuffer);
  txState = TX_SENDING;
  Serial.println("TX: Sent command");
}

void updateTxState() {
  switch (txState) {
    case TX_IDLE:
      break;

    case TX_SENDING:
      if (!Mirf.isSending()) {
        txStartTime = millis();
        txState = TX_WAIT_ACK;
      }
      break;

    case TX_WAIT_ACK:
      if (Mirf.dataReady()) {
        Mirf.getData((byte*)&reply);
        if (reply.type == ACK && reply.id == txBuffer.id) {
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
          Mirf.send((byte*)&txBuffer);
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
  Mirf.setTADDR((byte *)"robot");
  Mirf.setRADDR((byte *)"base");
  Mirf.channel = 90;
  Mirf.payload = sizeof(ServoCommand);
  Mirf.config();
}

void loop() {
 if (txState == TX_IDLE) {
    ServoCommand cmd = {CMD, ID, {'T','X','0'}, 123.4, 0};
    startTx(cmd);
  }
  updateTxState();
}
