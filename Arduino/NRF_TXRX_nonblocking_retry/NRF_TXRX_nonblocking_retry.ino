#include <SPI.h>
#include "Mirf.h"
#include "nRF24L01.h"
#include "MirfHardwareSpiDriver.h"

#define ID 39
#define GREEN_LED_PIN A4
#define RED_LED_PIN A5
#define SIZE_OF_PAYLOAD 10

enum MessageType : byte { CMD = 1, ACK = 2, NACK = 3 };

struct ServoCommand {
  byte type;
  byte id;
  char joint[3];
  float angle;
  byte checksum;
};

Nrf24l Mirf = Nrf24l(9, 10);

byte computeChecksum(byte* data, int length) {
  byte sum = 0;
  for (int k = 0; k < length; k++) sum ^= data[k];
  return sum;
}

enum TxState { TX_IDLE, TX_SENDING, TX_WAIT_ACK };
TxState txState = TX_IDLE;

ServoCommand txBuffer, rxReply;
unsigned long txStartTime = 0;
const unsigned long ACK_TIMEOUT = 10;
int retryCount = 0;
const int MAX_RETRIES = 3;

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
        Mirf.getData((byte*)&rxReply);
        if (rxReply.type == ACK && rxReply.id == txBuffer.id) {
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

enum RxState { RX_IDLE, RX_RECEIVED, RX_RESPONDING };
RxState rxState = RX_IDLE;

ServoCommand received, reply;
bool replyInProgress = false;

void updateRxState() {
  switch (rxState) {
    case RX_IDLE:
      if (Mirf.dataReady()) {
        Mirf.getData((byte*)&received);
        rxState = RX_RECEIVED;
      }
      break;

    case RX_RECEIVED: {
      byte expected = computeChecksum((byte*)&received, sizeof(received) - 1);
      if (expected == received.checksum && received.type == CMD) {
        reply = {ACK, received.id, {'A','C','K'}, 0.0, 0};
        digitalWrite(GREEN_LED_PIN, HIGH);
        Serial.println("RX: Valid CMD received");
      } else {
        reply = {NACK, received.id, {'N','A','K'}, 0.0, 0};
        digitalWrite(RED_LED_PIN, HIGH);
        Serial.println("RX: Invalid packet");
      }
      reply.checksum = computeChecksum((byte*)&reply, sizeof(reply) - 1);
      Mirf.send((byte*)&reply);
      replyInProgress = true;
      rxState = RX_RESPONDING;
      break;
    }

    case RX_RESPONDING:
      if (!Mirf.isSending()) {
        replyInProgress = false;
        rxState = RX_IDLE;
      }
      break;
  }
}

int role = TX;  // Change to RX on receiver board

void setup() {
  Serial.begin(115200);
  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);
  digitalWrite(GREEN_LED_PIN, LOW);
  digitalWrite(RED_LED_PIN, LOW);

  Mirf.spi = &MirfHardwareSpi;
  Mirf.init();

  if (role == TX) {
    Mirf.setTADDR((byte *)"base");
    Mirf.setRADDR((byte *)"robot");
  } else {
    Mirf.setTADDR((byte *)"robot");
    Mirf.setRADDR((byte *)"base");
  }

  Mirf.channel = 90;
  Mirf.payload = SIZE_OF_PAYLOAD;
  Mirf.config();
}

void loop() {
  if (role == TX) {
    if (txState == TX_IDLE) {
      ServoCommand cmd = {CMD, ID, {'T','X','0'}, 123.4, 0};
      startTx(cmd);
    }
    updateTxState();
  }

  if (role == RX) {
    updateRxState();
  }
}
