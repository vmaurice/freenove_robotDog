/*
    Video: https://www.youtube.com/watch?v=oCMOYS71NIU
    Based on Neil Kolban example for IDF: https://github.com/nkolban/esp32-snippets/blob/master/cpp_utils/tests/BLE%20Tests/SampleNotify.cpp
    Ported to Arduino ESP32 by Evandro Copercini
    updated by chegewara

   Create a BLE server that, once we receive a connection, will send periodic notifications.
   The service advertises itself as: 4fafc201-1fb5-459e-8fcc-c5c9c331914b
   And has a characteristic of: beb5483e-36e1-4688-b7f5-ea07361b26a8

   The design of creating the BLE server is:
   1. Create a BLE Server
   2. Create a BLE Service
   3. Create a BLE Characteristic on the Service
   4. Create a BLE Descriptor on the characteristic
   5. Start the service.
   6. Start advertising.

   A connect hander associated with the server starts a background task that performs notification
   every couple of seconds.
*/
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic_x = NULL;
BLECharacteristic* pCharacteristic_y = NULL;
BLECharacteristic* pCharacteristic_z = NULL;
bool deviceConnected = false;
bool oldDeviceConnected = false;

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/

//#define SERVICE_UUID_JOYSTICK               "a4b2b621-ef2b-42c8-adaf-35999ccea1e2"
//#define CHARACTERISTIC_UUID_JOYSTICK_X      "eec5d0af-64cf-44ea-a1d1-073ad823d69b"
//#define CHARACTERISTIC_UUID_JOYSTICK_Y      "01be4adc-ff2c-421a-886b-52e2e677bc5c"
//#define CHARACTERISTIC_UUID_JOYSTICK_Z      "d1f70ce0-bc31-48a9-a115-3253bc2bdb04"

#define SERVICE_UUID_JOYSTICK               "2A9F" // user control point
#define CHARACTERISTIC_UUID_JOYSTICK_X      "2AAE" // latitude
#define CHARACTERISTIC_UUID_JOYSTICK_Y      "2AAF" // longitude
#define CHARACTERISTIC_UUID_JOYSTICK_Z      "2AB3" // altitude


class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
      BLEDevice::startAdvertising();
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
    }
};

// GPIO init
int VRx = 36;
int VRy = 39;
int MS = 32;

void getJoystick() {
  uint8_t x, y ,z;
  x = map(analogRead(VRx),0,4096,0,255);
  y = map(analogRead(VRy),0,4096,0,255);
  z = digitalRead(MS);

  Serial.print("x: ");
  Serial.print(x);
  Serial.print(", y: ");
  Serial.print(y);
  Serial.print(", z: ");
  Serial.println(z);
  
  pCharacteristic_x->setValue(&x, 1);
  pCharacteristic_y->setValue(&y, 1);
  pCharacteristic_z->setValue(&z, 1);
}


void setup() {
  Serial.begin(115200);

  // Create the BLE Device
  BLEDevice::init("MyESP32");

  // Create the BLE Server
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());

  // Create the BLE Service
  BLEService *pService_joystick = pServer->createService(SERVICE_UUID_JOYSTICK);

  // Create a BLE Characteristic
  pCharacteristic_x = pService_joystick->createCharacteristic(
                      CHARACTERISTIC_UUID_JOYSTICK_X,
                      BLECharacteristic::PROPERTY_READ
                    );

  pCharacteristic_y = pService_joystick->createCharacteristic(
                      CHARACTERISTIC_UUID_JOYSTICK_Y,
                      BLECharacteristic::PROPERTY_READ
                    );

  pCharacteristic_z = pService_joystick->createCharacteristic(
                      CHARACTERISTIC_UUID_JOYSTICK_Z,
                      BLECharacteristic::PROPERTY_READ
                    );                                   

  // https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.descriptor.gatt.client_characteristic_configuration.xml
  // Create a BLE Descriptor
  pCharacteristic_x->addDescriptor(new BLE2902());
  pCharacteristic_y->addDescriptor(new BLE2902());
  pCharacteristic_z->addDescriptor(new BLE2902());

  // Start the service
  pService_joystick->start();

  // Start advertising
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID_JOYSTICK);
  pAdvertising->setScanResponse(false);
  pAdvertising->setMinPreferred(0x0);  // set value to 0x00 to not advertise this parameter
  BLEDevice::startAdvertising();


  analogReadResolution(12);

  pinMode(MS,INPUT);
  
  Serial.println("Ready");
}

void loop() {
    // notify changed value
    if (deviceConnected) {
        getJoystick();
        //pCharacteristic->notify();
        delay(100);
    }
    // disconnecting
    if (!deviceConnected && oldDeviceConnected) {
        delay(500); // give the bluetooth stack the chance to get things ready
        pServer->startAdvertising(); // restart advertising
        Serial.println("start advertising");
        oldDeviceConnected = deviceConnected;
    }
    // connecting
    if (deviceConnected && !oldDeviceConnected) {
        // do stuff here on connecting
        oldDeviceConnected = deviceConnected;
    }
}
