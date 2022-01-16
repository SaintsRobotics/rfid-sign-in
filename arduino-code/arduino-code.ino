#include <Wire.h>
#include <SPI.h>
#include <Adafruit_PN532.h>

// If using the breakout with SPI, define the pins for SPI communication.
#define PN532_SCK  (2)
#define PN532_MOSI (3)
#define PN532_SS   (4)
#define PN532_MISO (5)

// If using the breakout or shield with I2C, define just the pins connected
// to the IRQ and reset lines.  Use the values below (2, 3) for the shield!
#define PN532_IRQ   (2)
#define PN532_RESET (3)  // Not connected by default on the NFC Shield

// Uncomment just _one_ line below depending on how your breakout or shield
// is connected to the Arduino:

// Use this line for a breakout with a SPI connection:
Adafruit_PN532 nfc(PN532_SCK, PN532_MISO, PN532_MOSI, PN532_SS);

// Use this line for a breakout with a hardware SPI connection.  Note that
// the PN532 SCK, MOSI, and MISO pins need to be connected to the Arduino's
// hardware SPI SCK, MOSI, and MISO pins.  On an Arduino Uno these are
// SCK = 13, MOSI = 11, MISO = 12.  The SS line can be any digital IO pin.
//Adafruit_PN532 nfc(PN532_SS);

// Or use this line for a breakout or shield with an I2C connection:
//Adafruit_PN532 nfc(PN532_IRQ, PN532_RESET);

void setup(void) {
  Serial.begin(115200);
  while (!Serial) delay(10); // for Leonardo/Micro/Zero

  Serial.println("Hello!");

  nfc.begin();

  uint32_t versiondata = nfc.getFirmwareVersion();
  if (! versiondata) {
    Serial.print("Didn't find PN53x board");
    while (1); // halt
  }
  // Got ok data, print it out!
  Serial.print("Found chip PN5"); Serial.println((versiondata>>24) & 0xFF, HEX); 
  Serial.print("Firmware ver. "); Serial.print((versiondata>>16) & 0xFF, DEC); 
  Serial.print('.'); Serial.println((versiondata>>8) & 0xFF, DEC);
  
  // configure board to read RFID tags
  nfc.SAMConfig();
  
  Serial.println("Waiting for an ISO14443A Card ...");
}

uint8_t keya[6] = { 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF };
uint8_t i = 0;
uint8_t data[16]; //read to this buffer
uint8_t write_data[] = { i,'s','a','i','n','t','s',0, 0, 0, 0, 0, 0, 0, 0, 0 }; //data to write

void readAndWriteString() {
  Serial.println("read and write string called");
  Serial.setTimeout(3000); //10 seconds wait
  while(true) {
      String incomingString = Serial.readString();
      Serial.println(incomingString);
  }
  Serial.println("read and write string done");
}

void loop(void) {
  readAndWriteString();
  uint8_t success;
  uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };  // Buffer to store the returned UID
  uint8_t uidLength;                       // Length of the UID (4 or 7 bytes depending on ISO14443A card type)

  write_data[0] = i;
  i+=1;
  //uint8_t write_data[] = { i,'s','a','i','n','t','s',0, 0, 0, 0, 0, 0, 0, 0, 0 }; //data to write

//check if id is right
  if (nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength)) {
    //auth block
    if (nfc.mifareclassic_AuthenticateBlock(uid, uidLength, 4, 0, keya)) {
        Serial.print("block authenticated: \n");
        //read block
        if (nfc.mifareclassic_ReadDataBlock(4, data))
        {
          // Data seems to have been read ... spit it out
          Serial.println("Reading [INITIAL]:");
          nfc.PrintHexChar(data, 16);
          Serial.println("");
      
          // Wait a bit before reading the card again
          delay(1000);
        }
        
        //write data
        
        if (nfc.mifareclassic_WriteDataBlock (4, write_data)) {
          Serial.println("data written!");
          Serial.println("");
          delay(1000);
        }
        if (nfc.mifareclassic_ReadDataBlock(4, data))
        {
          Serial.println("Reading [SECOND]:");
          nfc.PrintHexChar(data, 16);
          Serial.println("");
          delay(1000);
        }
    }

    Serial.println("");
  }

};
