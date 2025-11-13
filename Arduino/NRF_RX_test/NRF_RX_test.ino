#include <SPI.h>
#include "Mirf.h"
#include "nRF24L01.h"
#include "MirfHardwareSpiDriver.h"

#define GREEN_LED_PIN A4
#define RED_LED_PIN A5

#define DEBUG_PRINT_STATEMENTS true

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
  char joint[3];
  float angle;
  byte checksum;
};

enum RxState { RX_IDLE, RX_RESPONDING };
RxState rxState = RX_IDLE;

Nrf24l Mirf = Nrf24l(9, 10);
ServoCommand received;
ServoCommand reply; // ACK packet for receiver
bool sendInProgress = false;

byte computeChecksum(byte* data, int length) 
{
  byte sum = 0;
  for (int k = 0; k < length; k++) sum ^= data[k];
  return sum;
}

void setup() 
{
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
          digitalWrite(RED_LED_PIN, HIGH);
        } 
        else 
        {
          reply = {NACK, received.id, {'N', 'A', 'K'}, 0.0, 0};
          if(DEBUG_PRINT_STATEMENTS) Serial.println("RX: Checksum mismatch");
          digitalWrite(RED_LED_PIN, LOW);
        }

        sendNRF(reply);
        rxState = RX_RESPONDING;
      }
      break;

    case RX_RESPONDING:
      digitalWrite(GREEN_LED_PIN, HIGH);
      sendNRF(reply);  // continue polling until done
      if (!sendInProgress) 
      {
        rxState = RX_IDLE;
        digitalWrite(GREEN_LED_PIN, LOW);
      }
      break;
  }
}

void loop() 
{
  updateRxState();
}
