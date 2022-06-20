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

// Breakout with a SPI connection:
Adafruit_PN532 nfc(PN532_SCK, PN532_MISO, PN532_MOSI, PN532_SS);

const int SPEAKER_PIN = 8;

void setup(void)
{
  Serial.begin(115200);

  pinMode(SPEAKER_PIN, OUTPUT);

  nfc.begin();
  nfc.SAMConfig();
  startupNoise();
}

uint8_t keya[6] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF}; // for auth
uint8_t data[4];                                        // for reading
// uint8_t write_data[4] = {0}; //data to write - incrementor
uint8_t uid[] = {0, 0, 0, 0, 0, 0, 0}; // Buffer to store the returned UID
uint8_t uidLength;                     // Length of the UID (4 or 7 bytes depending on ISO14443A card type)

void loop(void)
{
  bool detect = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength);
  bool auth = nfc.mifareclassic_AuthenticateBlock(uid, uidLength, 4, 0, keya);
  bool read = nfc.mifareclassic_ReadDataBlock(4, data);

  if (detect && auth && read)
  {
    for (int i = 0; i < sizeof(data); i++)
    {
      Serial.print(data[i]);
      Serial.println();
    }
    successNoise();
  }
  else
  {
    failNoise();
  }

  // this delay is necessary but adds far too much latency if misconfigured - stay around 500ms
  delay(1500);
}

void startupNoise()
{
  tone(SPEAKER_PIN, 1760, 50);
  delay(50);
  tone(SPEAKER_PIN, 2217, 50);
  delay(50);
  tone(SPEAKER_PIN, 2637, 50);
}

void successNoise()
{
  tone(SPEAKER_PIN, 880, 150);
}

void failNoise()
{
  tone(SPEAKER_PIN, 700, 150);
  delay(175);
  tone(SPEAKER_PIN, 700, 150);
}