#include <WiFi.h>
#include <WiFiUDP.h>
#include <esp_wifi.h> 

WiFiUDP udp;
const char * udpAddress = "255.255.255.255";
const int udpPort = 4444;
const int WIFI_CHANNEL = 6;

void setup() {
  Serial.begin(115200); // จอภาพฝั่ง Tx ไม่ได้แสดงผลอะไรเยอะ ใช้ความเร็วปกติได้
  Serial.println("Starting ESP32 Transmitter (AP Mode) for CSI...");

  // เปิดโหมด AP และ ล็อกช่องสัญญาณ
  WiFi.mode(WIFI_AP);
  WiFi.softAP("CSI_TX_ESP32", "12345678", WIFI_CHANNEL, 0);

  // บังคับแบนด์วิดท์เป็น 20 MHz (HT20)
  esp_wifi_set_bandwidth(WIFI_IF_AP, WIFI_BW_HT20);

  // ปิดโหมดประหยัดพลังงาน เพื่อให้ส่งคลื่นได้เต็มกำลัง
  esp_wifi_set_ps(WIFI_PS_NONE);

  udp.begin(udpPort);
  Serial.println("Tx Ready! Broadcasting continuous UDP packets at 100Hz...");
}

void loop() {
  unsigned long startMillis = millis();

  // สั่งยิงแพ็กเกจข้อมูลออกไปในอากาศ
  udp.beginPacket(udpAddress, udpPort);
  udp.printf("CSI_PING"); 
  udp.endPacket();

  // การหน่วงเวลาแบบชดเชยเวลาประมวลผล (10 มิลลิวินาที = 100 Hz)
  while (millis() - startMillis < 10) {
    vTaskDelay(1); 
  }
}