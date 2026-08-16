# 🍔 CampusEats

> **CS543 – Web Services & APIs | Assignment 1**

CampusEats is a campus food-ordering system designed to make ordering food easier for students. The system allows students to browse restaurants and menus, add food items to a cart, place orders, make payments, track deliveries, and receive notifications about their orders.

This repository contains our group's work for the CS543 assignment and documents the initial analysis and experiments that will help us build the CampusEats system in later stages.

---

## 👥 Team Members

| Name | Role | Enrollment No. | 
|---|---|---|
| **Siddiqui Md Sahil** | Team Leader | 20252651055 |
| **Ritik Kumar Sinha** | Team Member | 20252651043 |
| **Jeeshan Adil** | Team Member | 20252651026 |
| **Kruti Kansagara** | Team Member | 20252651027 |

We divided the assignment into different tasks so that each member could contribute to the project. The work and changes are recorded through Git commits in this repository.

---

## 🎯 Project Overview

The main idea behind CampusEats is to provide a simple food-ordering platform for students on campus.

A student should be able to:

- 🍽️ Browse restaurants and available menus
- 🔎 View food items and prices
- 🛒 Add items to a cart
- 📦 Place and check orders
- 💳 Make payments and handle refunds
- 🛵 Track food delivery
- 🔔 Receive notifications and order updates
- 👤 Manage profile and delivery addresses

These requirements will later help us identify the different capabilities and services of the CampusEats system.

---

## 📚 Assignment 1

This assignment focuses on understanding the basic concepts required before building the CampusEats services.

Our work includes:

### 🌐 1. HTTP Request/Response Log

We used `curl` to send HTTP requests to a public JSON API and recorded the responses.

The experiments include:

- GET requests
- HTTP status codes
- Response headers
- `Content-Type`
- JSON response bodies
- A deliberately invalid request resulting in `404 Not Found`

📄 See: [`docs/http-log.md`](docs/http-log.md)

---

### 📊 2. Browser Network Analysis

We used Google Chrome DevTools to observe the network activity of a webpage.

The analysis records:

- Total number of requests
- Total transferred data
- Total resource size
- Page loading timings
- Slowest resource
- 3xx/4xx responses

📄 See: [`docs/network-analysis.md`](docs/network-analysis.md)

---

### 📝 3. CampusEats System Brief

We identified the basic requirements of the CampusEats system by looking at:

- **WHAT** the system does
- **WHO** interacts with it
- Important **NOUNS** in the system
- Important **VERBS/actions** performed by the system

This gives us a starting point for identifying capabilities and services in the next assignment.

📄 See: [`docs/brief.md`](docs/brief.md)

---


### 📝 4. Work Distribution

- **Sahil**   → Repository setup & README + integration
- **Ritik**   → HTTP request response log
- **Jeeshan** → browser network analysis
- **Kruti**   → CampusEats system brief

---

## 📁 Repository Structure

```text
campuseats/
│
├── README.md
│
└── docs/
    ├── brief.md
    ├── http-log.md
    └── network-analysis.md


