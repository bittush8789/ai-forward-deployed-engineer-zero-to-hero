# Module 6: Supply Chain Logistics, WMS Systems & Control Towers

## 1. Industry Overview
Supply Chain management oversees the end-to-end flow of raw materials, components, and finished goods. The logistics lifecycle spans **Procurement** (sourcing raw materials), **Manufacturing** (processing goods), **Warehousing** (storing stock), and **Transportation** (shipping goods across distribution channels).

```
+-------------------------------------------------------------------------------------------------+
|                                        Supply Chain Flow                                        |
|                                                                                                 |
|   +------------+      +---------------+      +-------------+      +------------+      +--------+|
|   |  Supplier  | ---> |  Manufacturer | ---> |  Warehouse  | ---> |  Retailer  | ---> |Customer||
|   |  (Raw mat) |      |  (Assemble)   |      |  (Storage)  |      |  (Sales)   |      |  (Buy) ||
|   +------------+      +---------------+      +-------------+      +------------+      +--------+|
+-------------------------------------------------------------------------------------------------+
```

---

## 2. Revenue Model
Logistics and supply chain providers generate revenue from:
*   **Freight Charges**: Billing shippers for transporting goods across networks.
*   **Warehousing Fees**: Charging tenants for storage space and picking services.

---

## 3. Cost Structure
Supply chain operations' major costs include:
*   **Fuel & Transportation**: Cost of diesel, air freight, or ocean shipping.
*   **Labor Costs**: Salaries for warehouse workers and truck drivers.
*   **Storage Overhead**: Warehouse leases, energy bills, and automated picking systems maintenance.

---

## 4. Core Business Processes
*   **Inbound Logistics**: Receiving and warehousing goods from suppliers.
*   **Outbound Logistics**: Packaging and shipping finished goods.
*   **Inventory Replenishment**: Triggering restocking orders based on safety stock thresholds.
*   **Carrier Selection**: Booking carriers and negotiating freight rates.

---

## 5. Organizational Structure
*   **Supply Chain Director**: Oversees logistics, inventory health, and delivery timelines.
*   **Logistics Operations**: Manages carrier bookings, scheduling, and routing.
*   **Warehouse Operations**: Manages picking, packing, and sorting operations.
*   **Procurement**: Negotiates pricing with suppliers.

---

## 6. Enterprise Systems
*   **Warehouse Management Systems (WMS)**: Tracks active stock coordinates and pick list routing inside warehouses.
*   **Transportation Management Systems (TMS)**: Manages carrier routing, tracking, and billing.
*   **Enterprise Resource Planning (ERP)**: Central database tracking financials, purchasing, and logistics.

---

## 7. KPIs & Metrics
*   **On-Time In-Full (OTIF)**: Percentage of deliveries made within the scheduled window containing all ordered items.
*   **Lead Time**: Duration from order placement to customer delivery.
*   **Inventory Turnover**: COGS divided by average inventory value. Measures inventory efficiency.
*   **Fill Rate**: Percentage of customer orders fulfilled immediately from stock.

---

## 8. Regulatory Considerations
*   **Customs & Import Rules**: Enforcing international trade compliance.
*   **Driver HOS (Hours of Service) Rules**: Enforcing safety rest mandates on commercial drivers.

---

## 9. Business Challenges
*   **Global Logistics Disruptions**: Weather events or shipping delays disrupt inventory flows.
*   **Inefficient Routing**: Poor carrier routing increases fuel consumption and delivery times.

---

## 10. AI Opportunities

### Route Optimization & Control Towers
*   **Route Optimization**: Optimizing carrier routes based on traffic, weather, and pickup windows.
*   **Supply Chain Control Tower**: Centralizing data streams from WMS/TMS systems to track deliveries and flag anomalies in real-time.
*   **Supplier Risk Assessment**: Analyzing news and weather data to identify and mitigate supplier risks.

---

## 11. AI Use Cases
*   **Route Optimization**: Optimizing delivery routes for local package couriers.
*   **Control Tower**: Detecting delivery delays in transit and alerting logistics teams automatically.

---

## 12. Stakeholder Mapping

| Role | Business Goal | Operational Pain Point | AI Opportunity |
|---|---|---|---|
| **Supply Chain Director** | Maximize OTIF and minimize inventory costs | Global disruptions disrupt inventory flows | Supply Chain Control Tower |
| **Logistics Manager** | Reduce transit times and fuel costs | Poor carrier routing increases delivery times | Route Optimization |
| **Procurement Lead** | Settle supplier disputes and ensure pricing | Manual billing audits and pricing variations | Automated billing audit |

---

## 13. Discovery Workshops

### Discovery Questions
*   "What data sources are used to track active shipments?" (Maps data availability).
*   "Where do delays occur during order fulfillment?" (Identifies process bottlenecks).
*   "How are carrier routing decisions made?" (Identifies route optimization opportunities).

---

## 14. Case Studies

### Supply Chain Control Tower at Unilever
Unilever deployed an AI-powered supply chain control tower. By integrating real-time telemetry from WMS and TMS systems, the platform predicted delivery delays, allowing logistics teams to reschedule shipments, improving OTIF metrics.

---

## 15. Business Value Measurement
*   **OTIF Metric Improvement**: Track the increase in on-time, in-full deliveries.
*   **Reduction in Transit Costs**: Measure fuel and carrier booking savings.
*   **Decrease in Lead Times**: Track order-to-delivery speed improvements.

---

## 16. AI FDE Perspective

### Integrating AI with WMS & TMS Systems
As an AI Forward Deployed Engineer (FDE), you often integrate AI models with legacy WMS databases:
*   **WMS Integration**: Connect prediction outputs to WMS systems to trigger replenishment orders:
    ```python
    # API update payload config
    # Requests.post("https://core-wms.corp.local/api/orders/reorder")
    ```
Ensure data transformations are schema-compliant to prevent database write failures.
