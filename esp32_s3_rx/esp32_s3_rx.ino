#include <WiFi.h>
#include <esp_wifi.h>

// ฟังก์ชัน Callback พ่นข้อมูลออกหน้าจอ
void wifi_csi_rx_cb(void *ctx, wifi_csi_info_t *data) {
  wifi_pkt_rx_ctrl_t *mac_hdr = &data->rx_ctrl;
  int8_t rssi = mac_hdr->rssi;
  
  Serial.print("CSI_DATA,");
  Serial.print(rssi);
  Serial.print(",");
  
  for (int i = 0; i < data->len; i++) {
    Serial.print(data->buf[i]);
    if (i < data->len - 1) Serial.print(",");
  }
  Serial.println();
}

void setup() {
  // อัปเกรด Baud Rate เป็น 921600 เพื่อระบายข้อมูล 100Hz ให้ทัน
  Serial.begin(921600);
  Serial.println("Starting ESP32-S3 Receiver...");

  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  
  // ปิดโหมดประหยัดพลังงานฝั่งรับ
  esp_wifi_set_ps(WIFI_PS_NONE);

  Serial.print("Connecting to Tx...");
  WiFi.begin("CSI_TX_ESP32", "12345678");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to Tx!");

  // ล็อกช่องสัญญาณเป็นช่อง 6 ให้ตรงกับ Tx
  esp_wifi_set_channel(6, WIFI_SECOND_CHAN_NONE);

  // เปิดใช้งานโหมดดักจับสัญญาณและตั้งค่า CSI
  esp_wifi_set_promiscuous(true);
  esp_wifi_set_csi_rx_cb(&wifi_csi_rx_cb, NULL);
  
  wifi_csi_config_t csi_config = {
      .lltf_en = true,
      .htltf_en = true,
      .stbc_htltf2_en = true,
      .ltf_merge_en = true,
      .channel_filter_en = true,
      .manu_scale = false,
      .shift = false
  };
  esp_wifi_set_csi_config(&csi_config);
  esp_wifi_set_csi(true);
}

void loop() {
  delay(1000);
}