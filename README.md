# 📊 SBI Info API

> **Admin & Credits:** [t.me/EVILTALKS](https://t.me/EVILTALKS)

A lightning-fast, serverless Data Search API built with **FastAPI** and hosted on **Vercel**. This API allows you to search through massive JSON datasets (like SBI databases) by email, phone number, ID, password, or any other field instantly.

## 🚀 Features
- **Deep Search:** Searches across all fields in the JSON (including passwords, merchant IDs, emails, and names).
- **Raw Data Output:** Returns the exact object from the JSON file with zero data loss.
- **Serverless:** Runs completely on Vercel's free tier.
- **Branded:** Custom headers and endpoint responses powered by `t.me/EVILTALKS`.

---

## 🛠️ API Endpoints

### 1. Home / Health Check
Returns the status of the API and the total number of records loaded into memory.
- **URL:** `/`
- **Method:** `GET`

### 2. Deep Search
Search for any value across all JSON files. It will return up to 100 matching records.
- **URL:** `/api/search?q={query}`
- **Method:** `GET`
- **Examples:**
  - Search by Email: `https://sbiinfoapi.vercel.app/api/search?q=mani04081987@yahoo.com`
  - Search by Phone: `https://sbiinfoapi.vercel.app/api/search?q=9962266009`
  - Search by ID: `https://sbiinfoapi.vercel.app/api/search?q=13626`

### 3. Get Record by Exact ID
Fetches a specific record using its exact `id` field.
- **URL:** `/api/record/{id}`
- **Method:** `GET`
- **Example:** `https://sbiinfoapi.vercel.app/api/record/13626`

---

## 📂 Project Structure
To deploy this yourself, your project must be structured exactly like this:

```text
sbi-info-api/
├── api/
│   └── index.py          # The FastAPI application
├── data/
│   ├── sbi1.json         # Put all your JSON files here
│   ├── sbi2.json
│   └── sbi3.json
├── requirements.txt      # Python dependencies
└── vercel.json           # Vercel routing configuration
