# 💧 AI-Cloud-IoT Water Quality Monitoring System

An end-to-end, automated hardware and software solution that transitions water quality management from manual sampling to real-time, predictive environmental monitoring[cite: 3]. 

## 📖 Project Overview
Conventional water testing relies on expensive, time-consuming laboratory analysis[cite: 3]. This project solves that latency by deploying a continuous edge-to-cloud pipeline[cite: 3]. It utilizes IoT sensors to gather physical data, cloud platforms for secure data transmission, and machine learning models to classify water health and predict contamination events before they escalate[cite: 3].

## 🚀 Key Achievements & Impact
*   **High-Accuracy ML Predictions:** Achieved up to 94% accuracy in forecasting long-term contamination trends using historical data modeling[cite: 3]. 
*   **Real-Time Latency:** Engineered a system with less than 5 seconds of delay between a physical water quality change and its reflection on the cloud dashboard[cite: 3].
*   **Automated Emergency Response:** Implemented an alert engine that instantly triggers SMS/Email notifications to stakeholders if critical safety thresholds are breached[cite: 3].
*   **Published Research:** The architecture and findings of this system were published as first-author research. 

## 🛠️ Technical Architecture

This system is built across three distinct engineering layers:

### 1. Edge & Data Acquisition (Hardware)
*   **Microcontroller:** ESP32 acting as the primary edge processing node[cite: 3].
*   **Sensor Array:** High-precision probes measuring pH, Turbidity, Total Dissolved Solids (TDS), and Temperature (DS18B20)[cite: 3].
*   **Local Interface:** I2C-enabled LCD display for immediate, on-site data verification[cite: 3].

### 2. Networking & Cloud Integration
*   **Protocols:** Wi-Fi and MQTT for lightweight, reliable data packaging[cite: 3].
*   **Cloud Platform:** Integrated with ThingSpeak (and Firebase) for remote synchronization, secure database storage, and real-time telemetry dashboards[cite: 3].

### 3. Intelligence & Analytics Layer
*   **AI Models:** Random Forest and Long Short-Term Memory (LSTM) networks utilized for time-series forecasting and classification[cite: 3].
*   **Decision Logic:** Evaluates incoming multi-sensor data against learned patterns to automatically classify water as *Safe*, *Moderate*, or *Unsafe*[cite: 3].

## ⚙️ How to Run the Project

**1. Hardware Setup**
*   Connect the pH, Turbidity, TDS, and Temperature sensors to the ESP32 microcontroller as per the standard pinout configuration.
*   Power the ESP32 via USB or a dedicated 5V power supply.

**2. Software & Cloud Configuration**
*   Clone this repository: `git clone https://github.com/sana-tabasum/AI-Cloud-IoT-Water-Quality.git`
*   Open the `.ino` file in the Arduino IDE and input your local Wi-Fi credentials and ThingSpeak API keys.
*   Flash the C++ code to the ESP32.

**3. Launching the Analytics**
*   Navigate to the `analytics` folder and install dependencies: `pip install -r requirements.txt`
*   Run the main Python script to fetch the live cloud data and apply the classification models.
