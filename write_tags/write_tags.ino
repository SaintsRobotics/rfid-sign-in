#include <Wire.h>
#include <SPI.h>
#include <Adafruit_PN532.h>

// If using the breakout with SPI, define the pins for SPI communication.
#define PN532_SCK (2)
#define PN532_MOSI (3)
#define PN532_SS (4)
#define PN532_MISO (5)

// If using the breakout or shield with I2C, define just the pins connected
// to the IRQ and reset lines.  Use the values below (2, 3) for the shield!
#define PN532_IRQ (2)
#define PN532_RESET (3) // Not connected by default on the NFC Shield

// Use this line for a breakout with a SPI connection:
Adafruit_PN532 nfc(PN532_SCK, PN532_MISO, PN532_MOSI, PN532_SS);

uint32_t incrementor;
String tmp; // for reading from user and making sure actual input is read

void setup(void)
{
  Serial.begin(115200);

  Serial.println("starting");
  Serial.println("please input an initial value for incrementor - just entering will default to 0");

  while (true)
  {
    tmp = Serial.readString();
    if (tmp != "")
    {
      break;
    }
  }
  incrementor = tmp.toInt();

  if (incrementor == 0)
  {
    Serial.println("Starting at 0");
  }
  else
  {
    Serial.print("Starting count at ");
    Serial.println(incrementor);
  }

  pinMode(8, OUTPUT);

  nfc.begin();
  nfc.SAMConfig();
}

uint8_t keya[6] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF}; // for auth
uint8_t data[4];                                        // for reading
// uint8_t write_data[4] = {0}; //data to write - incrementor
uint8_t uid[] = {0, 0, 0, 0, 0, 0, 0}; // Buffer to store the returned UID
uint8_t uidLength;                     // Length of the UID (4 or 7 bytes depending on ISO14443A card type)
uint8_t write_data[4] = {0};

void loop(void)
{

  write_data[3] = incrementor;
  write_data[2] = incrementor >> 8;
  write_data[1] = incrementor >> 16;
  write_data[0] = incrementor >> 24;

  if (nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength))
    // auth block
    if (nfc.mifareclassic_AuthenticateBlock(uid, uidLength, 4, 0, keya))
    {
      // Serial.print("[block authenticated]\n");
      //  read block
      if (nfc.mifareclassic_ReadDataBlock(4, data))
      {
        // Data seems to have been read ... spit it out
        Serial.println("[reading]: ");
        nfc.PrintHexChar(data, 4);
        Serial.println();

        // Wait a bit before reading the card again
        delay(1000);
      }

      // write data
      if (nfc.mifareclassic_WriteDataBlock(4, write_data))
      {
        Serial.println("data written!\n");
        delay(1000);
      }
      if (nfc.mifareclassic_ReadDataBlock(4, data))
      {
        Serial.println("[reading again for sanity]: ");
        nfc.PrintHexChar(data, 4);
        Serial.println();
        delay(1000);
      }
      /*if (nfc.mifareclassic_AuthenticateBlock(uid, uidLength, 9, 0, keya))
          {
            if (nfc.mifareclassic_WriteDataBlock(9, write_data))
            {
              Serial.println("[saints data written]\n");
              delay(500);
            }
          }*/
    }

  Serial.print("[done] with ");
  Serial.println(incrementor);
  /*while (true) {
           tmp = Serial.readString();
           if (tmp != "") {
            break;
           }
        }*/
  tone(8, 880, 300);
  delay(3000);
  incrementor += 1;
}
