#include <ADCInput.h>

#define W_CLK 2    // AD9850 word load clock pin
#define FQ_UD 3    // AD9850 frequency update pin
#define DATA 4     // AD9850 serial data pin
#define RESET 5    // AD9850 reset pin

#define pulseHigh(pin) { digitalWrite(pin, HIGH); digitalWrite(pin, LOW); }

ADCInput analog(A2);   // Initialize ADC on A2

// Function to transfer a byte to AD9850 (LSB first)
void tr_byte(byte data) {
    for (int i = 0; i < 8; i++, data >>= 1) {
        digitalWrite(DATA, data & 0x01);
        pulseHigh(W_CLK); // Pulse W_CLK after sending each bit
    }
}

// Function to calculate and send frequency to AD9850
void sendFrequency(double frequency) {
    unsigned long freq = frequency * 4294967295 / 125000000.0; // Convert to 32-bit tuning word
    for (int b = 0; b < 4; b++, freq >>= 8) {
        tr_byte(freq & 0xFF);
    }
    tr_byte(0x00);   // Final control byte (all 0s for AD9850)
    pulseHigh(FQ_UD); // Update frequency output
}

void setup() {
    Serial.begin(115200);
    analog.begin(500000);   // ADC sampling rate 500 kHz

    // Configure AD9850 control pins as outputs
    pinMode(FQ_UD, OUTPUT);
    pinMode(W_CLK, OUTPUT);
    pinMode(DATA, OUTPUT);
    pinMode(RESET, OUTPUT);

    // Initialize AD9850 with reset pulses
    pulseHigh(RESET);
    pulseHigh(W_CLK);
    pulseHigh(FQ_UD);
}

void loop() {
    for (int f = 50000; f <= 300000; f += 1000) {  // Sweep from 50kHz to 300kHz (step 1kHz)
        sendFrequency(f); // Set AD9850 output frequency

        int maxReading = 0;

        // Capture 500 ADC samples and record the maximum value
        for (int i = 0; i < 500; i++) {
            int val = analog.read();
            if (val > maxReading) {
                maxReading = val;
            }
        }

        Serial.print(maxReading);
        Serial.print(", ");   // Print values in CSV format
    }

    Serial.println(); // New line after frequency sweep
}
