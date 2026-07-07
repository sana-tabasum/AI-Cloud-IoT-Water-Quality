# 💧 AI-Cloud-IoT Water Quality Monitoring System.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![MQTT](https://img.shields.io/badge/Protocol-MQTT-purple.svg)](https://mqtt.org/)
[![AWS](https://img.shields.io/badge/Cloud-AWS-orange.svg)](https://aws.amazon.com/)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

An end-to-end **IoT + AI + Cloud** pipeline for real-time water quality monitoring. Sensor nodes stream **pH, turbidity, and TDS (Total Dissolved Solids)** readings over **MQTT** to **ThingSpeak** for live visualization, while a parallel ingestion service pushes the same telemetry to **AWS** for storage and batch analytics. A **Scikit-learn** classification model then evaluates water potability from the ingested readings.

> 📄 Companion research paper (first-author): *"An IoT-Integrated AI & Cloud-Based Approach for Water Quality Monitoring System."*

---

## 🚀 Key Features

- **Real-time sensing** — pH, turbidity, and TDS captured via analog/digital sensors on an Arduino/ESP32 node.
- **MQTT telemetry pipeline** — lightweight publish/subscribe messaging for low-latency, low-bandwidth transmission.
- **Live dashboards on ThingSpeak** — instant visualization and channel-based alerting.
- **Cloud persistence on AWS** — readings archived to S3 (and optionally DynamoDB) for long-term analysis.
- **ML-based potability classification** — a Scikit-learn model flags unsafe readings using standard water-quality thresholds.
- **Modular, testable codebase** — ingestion, cloud, and modeling layers are fully decoupled.

---

## 🏗️ System Architecture

```
┌────────────────────┐        MQTT         ┌──────────────────┐
│  Sensor Node        │ ───────────────────▶│  MQTT Broker      │
│  (Arduino/ESP32)     │   pH · Turbidity ·   │  (e.g. Mosquitto) │
│  hardware/sensor_    │   TDS  every N sec   └────────┬─────────┘
│  reader.ino           │                              │
└────────────────────┘                              │
                                                       ▼
                              ┌────────────────────────────────────┐
                              │  MQTT Subscriber (Python)            │
                              │  src/data_ingestion/mqtt_client.py   │
                              └───────┬───────────────────┬─────────┘
                                      │                   │
                         ┌────────────▼─────┐   ┌─────────▼──────────┐
                         │  ThingSpeak Upload │   │  AWS S3 Uploader    │
                         │  (live dashboard)  │   │  src/cloud/aws_...  │
                         └───────────────────┘   └─────────┬──────────┘
                                                            │
                                                  ┌─────────▼──────────┐
                                                  │  ML Classifier       │
                                                  │  src/model/water_    │
                                                  │  quality_model.py    │
                                                  │  → Potable / Unsafe  │
                                                  └───────────────────┘
```

---

## 📁 Repository Structure

```
water-quality-monitoring/
├── hardware/
│   ├── sensor_reader.ino        # Arduino/ESP32 firmware: reads sensors, publishes over MQTT
│   └── wiring_diagram.md        # Pin mapping & circuit notes
├── src/
│   ├── data_ingestion/
│   │   └── mqtt_client.py       # Subscribes to broker, forwards readings downstream
│   ├── cloud/
│   │   └── aws_s3_handler.py    # Uploads/reads telemetry from AWS S3
│   ├── model/
│   │   ├── water_quality_model.py  # Model definition + inference
│   │   └── train.py                # Training script (Scikit-learn)
│   └── utils/
│       └── preprocessing.py     # Cleaning, feature engineering, thresholding
├── data/
│   └── sample_sensor_data.csv   # Example telemetry for offline testing/training
├── tests/
│   └── test_model.py            # Unit tests for the ML pipeline
├── config/
│   └── config.yaml              # Broker, AWS, and ThingSpeak configuration
├── main.py                      # Orchestrates ingestion → cloud → inference
├── requirements.txt
├── .gitignore
└── LICENSE
```

---

## ⚙️ Tech Stack

| Layer | Tools |
|---|---|
| Firmware | C++ (Arduino/ESP32), analog sensor drivers |
| Messaging | MQTT (Mosquitto / any broker) |
| Live Dashboard | ThingSpeak |
| Cloud | AWS (S3, optionally DynamoDB/Lambda) |
| ML | Python, Scikit-learn, Pandas, NumPy |
| Config | YAML |

---

## 🔧 Installation

```bash
git clone https://github.com/sana-tabasum/water-quality-monitoring.git
cd water-quality-monitoring
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Update `config/config.yaml` with your MQTT broker address, ThingSpeak channel/API key, and AWS credentials (or configure the AWS CLI / environment variables instead of hardcoding secrets).

---

## ▶️ Usage

**1. Flash the sensor node**
Upload `hardware/sensor_reader.ino` to your Arduino/ESP32 using the Arduino IDE, after editing the WiFi/MQTT broker credentials at the top of the file.

**2. Start the ingestion pipeline**
```bash
python main.py
```
This subscribes to the MQTT topic, streams readings to ThingSpeak, archives them to AWS S3, and runs each new reading through the potability classifier.

**3. Train the model on your own data**
```bash
python src/model/train.py --data data/sample_sensor_data.csv
```

**4. Run tests**
```bash
pytest tests/
```

---

## 📊 Sample Result

The classifier flags each reading as `Potable` or `Unsafe` based on pH, turbidity, and TDS thresholds learned from labeled samples, enabling automated alerts when water quality drifts outside safe bounds.

---

## 🧪 Parameters Monitored

| Parameter | Sensor | Safe Range (WHO guideline) |
|---|---|---|
| pH | Analog pH probe | 6.5 – 8.5 |
| Turbidity | Turbidity sensor (NTU) | < 5 NTU |
| TDS | TDS/conductivity sensor | < 500 ppm |

---

## 📄 Citation

If you use this work, please cite:

> Shaik, S. *An IoT-Integrated AI & Cloud-Based Approach for Water Quality Monitoring System.*

---

## 👩‍💻 Author

**Sana Shaik**
B.Tech CSE (AI & ML), Sreyas Institute of Engineering and Technology
[LinkedIn](https://linkedin.com/in/sana-tabassum) · [GitHub](https://github.com/sana-tabasum)

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
