#include <Arduino.h>
#include <BluetoothSerial.h>
#include <driver/i2s.h>

BluetoothSerial SerialBT;

// I2S Configuration (INMP441 / SPH0645)
#define I2S_WS   15  // LRCLK
#define I2S_SD   32  // Data in
#define I2S_SCK  14  // BCLK

void setupI2S() {
    i2s_config_t i2s_config = {
        .mode = i2s_mode_t(I2S_MODE_MASTER | I2S_MODE_RX),
        .sample_rate = 16000,
        .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
        .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
        .communication_format = i2s_comm_format_t(I2S_COMM_FORMAT_I2S_MSB),
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
        .dma_buf_count = 8,
        .dma_buf_len = 256,
        .use_apll = false
    };

    i2s_pin_config_t pin_config = {
        .bck_io_num = I2S_SCK,
        .ws_io_num = I2S_WS,
        .data_out_num = -1,
        .data_in_num = I2S_SD
    };

    i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
    i2s_set_pin(I2S_NUM_0, &pin_config);
    i2s_start(I2S_NUM_0);
}

void setup() {
    Serial.begin(115200);
    SerialBT.begin("ESP32-Audio");
    setupI2S();
    Serial.println("ESP32 Bluetooth Audio Streaming Started...");
}

void loop() {
    int16_t audioData[512];  // Use int16_t to match Vosk format
    size_t bytesRead;

    // Read PCM audio from I2S (16-bit data)
    i2s_read(I2S_NUM_0, audioData, sizeof(audioData), &bytesRead, portMAX_DELAY);

    if (bytesRead > 0) {
        int samples = bytesRead / sizeof(int16_t);

        // Debug: Print first few samples to Serial Monitor
        Serial.print("PCM Data: ");
        for (int i = 0; i < samples && i < 10; i++) {  // Print first 10 samples
            Serial.print(audioData[i]);
            Serial.print(" ");
        }
        Serial.println();

        // Send PCM data to Vosk via Bluetooth Serial
        SerialBT.write((uint8_t *)audioData, bytesRead);
    }

    delay(10); // Prevents Bluetooth buffer overflow
}
