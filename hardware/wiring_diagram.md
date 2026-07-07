# Wiring & Pin Mapping

## Components
- ESP32 (or ESP8266) development board
- Analog pH probe + amplifier board
- Turbidity sensor (analog output)
- TDS/conductivity sensor (analog output)
- Breadboard + jumper wires
- 5V power supply (USB or external)

## Pin Mapping (ESP32)

| Sensor | Sensor Pin | ESP32 Pin | Notes |
|---|---|---|---|
| pH probe amplifier | AO (analog out) | GPIO 34 | Analog-only input pin |
| pH probe amplifier | VCC / GND | 3.3V / GND | Check amplifier board voltage rating |
| Turbidity sensor | AO | GPIO 35 | Analog-only input pin |
| Turbidity sensor | VCC / GND | 5V / GND | Most turbidity boards need 5V |
| TDS sensor | AO | GPIO 32 | |
| TDS sensor | VCC / GND | 3.3V–5V / GND | Check module spec |

## Notes
- GPIO 34/35 on the ESP32 are **input-only** and ADC-capable — ideal for analog sensor reads.
- Keep sensor probes isolated from each other in the water sample to avoid cross-interference, especially between the pH and TDS probes.
- Calibrate each probe against known reference solutions (e.g., pH 4.0/7.0/10.0 buffer solutions; NTU turbidity standards) and update the calibration constants in `sensor_reader.ino` before deployment.
- For long cable runs to the probes, use shielded cable to reduce analog noise.
