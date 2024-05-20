#include "DFRobot_DF2301Q.h"

// I2C communication
DFRobot_DF2301Q_I2C DF2301Q;

void setup()
{
  Serial.begin(115200);

  // Init the sensor
  while( !( DF2301Q.begin() ) ) {
    Serial.println("Communication with device failed, please check connection");
    delay(3000);
  }
  Serial.println("Begin ok!");

  /**
   * @brief Set voice volume
   * @param voc - Volume value(1~7)
   */
  DF2301Q.setVolume(7);
  Serial.println("Volume set to 7");

  /**
   * @brief Set wake-up duration
   * @param wakeTime - Wake-up duration (0-255)
   */
  DF2301Q.setWakeTime(15);
  Serial.println("Wake-up time set to 15");

  /**
   * @brief Get wake-up duration
   * @return The currently-set wake-up period
   */
  uint8_t wakeTime = DF2301Q.getWakeTime();
  Serial.print("wakeTime = ");
  Serial.println(wakeTime);

  // Remove these lines for now to focus on receiving CMDID
  // DF2301Q.playByCMDID(1);   // Wake-up command
  // DF2301Q.playByCMDID(23);   // Common word ID
}

void loop()
{
  uint8_t CMDID = DF2301Q.getCMDID();
  
  if (0 != CMDID) {
    Serial.print("CMDID = ");
    Serial.println(CMDID);

    // Add more logic here to handle the received CMDID
  } else {
    //Serial.println("No valid CMDID received.");
  }

  // Add a small delay to avoid spamming the I2C bus
  delay(100);
}