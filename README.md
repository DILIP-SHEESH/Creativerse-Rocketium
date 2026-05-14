# Creativerse-Rocketium
### Automated Ad Review Tool

A web app that reviews ad creatives against brand guidelines and publishing platform rules at scale. Upload an image, get a compliance score, violation breakdown, and safety rating — without manual review.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://python.org/)
[![Flask](https://img.shields.io/badge/Backend-Flask-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![AWS](https://img.shields.io/badge/AWS-Rekognition%20%2B%20Bedrock-FF9900?logo=amazonaws&logoColor=white)](https://aws.amazon.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## What it does

Manually reviewing hundreds of ad creatives for compliance is slow and error-prone. This tool automates that process. Upload a creative, and the pipeline extracts visual and textual content from the image, checks it against your provided guidelines and platform rules (Facebook, Google, Instagram, etc.), and returns a structured review.

Each review includes:
- A compliance percentage
- A list of specific violations with feedback
- A safety rating (Safe / Not Safe)

---

## How it works

1. User uploads an ad image via the web interface.
2. **AWS Rekognition** extracts text from the image and detects labels and objects.
3. The extracted content is passed to **AWS Bedrock** (Meta Llama 3) along with the relevant brand and platform guidelines.
4. The LLM reviews the ad for compliance and returns a structured result with score, violations, and safety verdict.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Flask (Python) |
| Vision / OCR | AWS Rekognition |
| LLM Review | AWS Bedrock (Meta Llama 3) |
| AWS SDK | boto3 |
| Image Processing | Pillow |
| Frontend | HTML, CSS |

---

## Project Structure

```
Creativerse-Rocketium/
└── AdReview/
    ├── app.py              # Flask app, routes, AWS integration
    ├── templates/          # HTML frontend
    ├── static/             # CSS and assets
    └── requirements.txt
```

---

## Getting Started

**Prerequisites**

- Python 3.x
- AWS account with Rekognition and Bedrock access
- AWS credentials configured locally (`~/.aws/credentials` or environment variables)

**Setup**

```bash
git clone https://github.com/DILIP-SHEESH/Creativerse-Rocketium.git
cd Creativerse-Rocketium/AdReview
pip install -r requirements.txt
```

Set your AWS credentials:

```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=your_region
```

Run the app:

```bash
python app.py
```

Open `http://localhost:5000` in your browser.

---

## Use Cases

- Ad agencies reviewing creatives before submission to platforms
- Advertisers checking brand guideline compliance at scale
- Publishing platforms automating pre-moderation of ad inventory

---

## Status

Early stage. Core review pipeline is functional. Contributions and feedback welcome via [Issues](https://github.com/DILIP-SHEESH/Creativerse-Rocketium/issues).
