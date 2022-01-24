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

// Uncomment just _one_ line below depending on how your breakout or shield
// is connected to the Arduino:

// Use this line for a breakout with a SPI connection:
Adafruit_PN532 nfc(PN532_SCK, PN532_MISO, PN532_MOSI, PN532_SS);

// Use this line for a breakout with a hardware SPI connection.  Note that
// the PN532 SCK, MOSI, and MISO pins need to be connected to the Arduino's
// hardware SPI SCK, MOSI, and MISO pins.  On an Arduino Uno these are
// SCK = 13, MOSI = 11, MISO = 12.  The SS line can be any digital IO pin.
// Adafruit_PN532 nfc(PN532_SS);

// Or use this line for a breakout or shield with an I2C connection:
// Adafruit_PN532 nfc(PN532_IRQ, PN532_RESET);

uint32_t incrementor;
String tmp; //for reading from user and making sure actual input is read

void setup(void)
{
    Serial.begin(115200);

    pinMode(8, OUTPUT);
    //f
    tone(8, 880, 100);
    delay(100);
    tone(8, 880, 100);
    delay(100);
    tone(8, 880, 300);
    delay(100);
    tone(8, 880, 100);
    delay(100);
    delay(300);
    //u
    tone(8, 880, 100);
    delay(100);
    tone(8, 880, 100);
    delay(100);
    tone(8, 880, 300);
    delay(100);
    delay(300);
    //c
    tone(8, 880, 300);
    delay(100);
    tone(8, 880, 100);
    delay(100);
    tone(8, 880, 300);
    delay(100);
    tone(8, 880, 100);
    delay(100);
    delay(300);
    //k
    tone(8, 880, 300);
    delay(100);
    tone(8, 880, 100);
    delay(100);
    tone(8, 880, 300);
    delay(100);
    delay(300);
    //space
    delay(700);
    //y
    tone(8, 880, 300);
    delay(100);
    tone(8, 880, 100);
    delay(100);
    //o
    //u
    //dash
    tone(8, 880, 300);
    delay(100);
    //dot
    tone(8, 880, 100);
    delay(100);
    ..-...- -.-.-.- / -.-----..-

        nfc.begin();
    nfc.SAMConfig();
}

uint8_t keya[6] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF}; //for auth
uint8_t data[4];                                        //for reading
//uint8_t write_data[4] = {0}; //data to write - incrementor
uint8_t uid[] = {0, 0, 0, 0, 0, 0, 0}; // Buffer to store the returned UID
uint8_t uidLength;                     // Length of the UID (4 or 7 bytes depending on ISO14443A card type)

void loop(void)
{
    if (nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength))
        // auth block
        if (nfc.mifareclassic_AuthenticateBlock(uid, uidLength, 4, 0, keya))
        {
            //Serial.print("[block authenticated]\n");
            // read block
            if (nfc.mifareclassic_ReadDataBlock(4, data))
            {
                nfc.PrintHex(data, 4);
                //Serial.println();

                // Wait a bit before reading the card again
                delay(1000);
            }
        }
}
