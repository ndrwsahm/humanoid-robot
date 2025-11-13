#include <SPI.h>
#include "Mirf.h"
#include "nRF24L01.h"
#include "MirfHardwareSpiDriver.h"

#define ID 39
#define GREEN_LED_PIN A4
#define RED_LED_PIN A5

struct ServoCommand {
  byte type;
  byte id;
  char joint[3];
  float angle;
  byte checksum;
};

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

Nrf24l Mirf = Nrf24l(9, 10);
ServoCommand cmd = {1, ID, {'T','X','0'}, 123.4, 0};

byte computeChecksum(byte* data, int length) {
  byte sum = 0;
  for (int k = 0; k < length; k++) sum ^= data[k];
  return sum;
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
  cmd.checksum = computeChecksum((byte*)&cmd, sizeof(cmd) - 1);
  Mirf.send((byte*)&cmd);
  while (Mirf.isSending());

  Serial.println("TX: Sent command");
  digitalWrite(GREEN_LED_PIN, HIGH);
  delay(100);
  digitalWrite(GREEN_LED_PIN, LOW);
  delay(1000);  // Send every second
}
