#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <TFT_eSPI.h> // balle
#include <Wire.h> // chien 
#include <Adafruit_VL53L0X.h> // chien 


Adafruit_VL53L0X lox = Adafruit_VL53L0X(); // chien

TFT_eSPI tft; // balle

int message; //flag

BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;

char char_received = '0';
String fromSerial = "";
String valor;  // Déclarer valor en tant que variable globale
const int sensorPin = 36; // Broche du CAN0, à brancher sur le Out du capteur // balle
const float voltageConversion = 5 / 4095.0; // Conversion de la valeur analogique en tension (5V alimentation, résolution 12 bits) // balle

#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"


class MyCallbacks: public BLECharacteristicCallbacks {
    // RECEIVE NUMBER FROM APP (Slider).
    void onWrite(BLECharacteristic *pCharacteristic) {
      std::string value = pCharacteristic->getValue();
      
      if (value.length() > 0) {
        valor = "";
        for (int i = 0; i < value.length(); i++){
          valor = valor + value[i];          
        }
        message = 1;  //Quand on  a une valeur de l'appli on met le flag a 1
      }
    }
};


void setup() {
  Serial.begin(115200);

  // balle 
  pinMode(sensorPin, INPUT);

  // chien
  if (!lox.begin()) { 
    Serial.println(F("Impossible d'initialiser le VL53L0X"));
    delay(5000);  // Attendre 5 secondes avant de réinitialiser
    ESP.restart();  // Réinitialiser le microcontrôleur
    while (1); 
  }
  // Le capteur est initialisé
  Serial.println(F("VL53L0X trouvé !"));

  // BLE
  BLEDevice::init("EMMA&MARIE");
  pServer = BLEDevice::createServer();
  BLEService *pService = pServer->createService(SERVICE_UUID);
  pCharacteristic = pService->createCharacteristic(
                                         CHARACTERISTIC_UUID,
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_WRITE |
                                         BLECharacteristic::PROPERTY_NOTIFY |
                                         BLECharacteristic::PROPERTY_INDICATE
                                        );

  pCharacteristic->setCallbacks(new MyCallbacks());
  pService->start();

  BLEAdvertising *pAdvertising = pServer->getAdvertising();
  pAdvertising->start();
}

void loop() {
  
  //Get number from Serial Monitor.
  VL53L0X_RangingMeasurementData_t measure; // chien
  lox.rangingTest(&measure, false); // Perform a range measurement // chien
  int sensorValue = analogRead(sensorPin)/4095; // Lecture de la valeur analogique // balle
  if (message == 1) { // Si il y a une valeur dans message
    char_received = Serial.read(); // Recupère le caractère
    fromSerial += char_received;
    if (sensorValue==1) { // Si il n'y a pas de balle // balle

      // ON LANCE PAS LA BALLE
    } 
    else { // balle présente
      if (measure.RangeStatus != 4) {  // 4 signifie une mesure valide 
      // La mesure est valide
        if (measure.RangeMilliMeter > 300){
                   
        }
      }
      else { // Tout est ok
        Serial.print(1);
      }
      
  
      delay(250);  // Attendre un court instant entre les mesures
    } // balle
    Serial.print("\n\r"); // balle
    delay(1000); // Attendre 1 seconde entre les lectures // balle
    
  }  
  message = 0;
}
