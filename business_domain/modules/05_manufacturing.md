# Module 5: Manufacturing Operations, MES Controls & Predictive Maintenance

## 1. Industry Overview
Manufacturing involves transforming raw materials or components into finished products. The sector is divided into **Discrete Manufacturing** (assembling distinct, bill-of-materials items like cars or smartphones) and **Process Manufacturing** (blending raw ingredients using formulas like chemicals, pharmaceuticals, or food).

```
+-------------------------------------------------------------------------------------------------+
|                                        Manufacturing Flow                                       |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                     Material Inflow                                     |   |
|   |   - Raw materials and components are received and inspected                             |   |
|   +---------------------------------------+-------------------------------------------------+   |
|                                           |                                                     |
|                                           v (Production Routing)                                |
|   +---------------------------------------+-------------------------------------------------+   |
|   |                                     Assembly Line                                       |   |
|   |   - CNC machines, assembly lines, and robotics process components                       |   |
|   +-------------------+-------------------------------------------------+-------------------+   |
|                       | (Telemetry Logging)                             | (Outflow)             |
|                       v                                                 v                       |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|   |             SCADA System (Sensor Data)  |     |             Finished Goods              |   |
|   |   - Logs temperature, pressure, vibration|     |   - Inspected and shipped to customers  |   |
|   +-----------------------------------------+     +-----------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

---

## 2. Revenue Model
Manufacturers generate revenue from:
*   **Finished Goods Sales**: Selling assembled products directly to distributors, retailers, or consumers.
*   **Aftermarket Services**: Providing maintenance services and spare parts.

---

## 3. Cost Structure
Manufacturers' major costs include:
*   **Direct Materials**: Raw materials and components required for production.
*   **Direct Labor**: Salaries for assembly workers and operators.
*   **Overhead Costs**: Facility maintenance, utility costs, and factory machinery depreciation.

---

## 4. Core Business Processes
*   **Production Planning**: Scheduling assembly operations based on demand forecasts.
*   **Procurement**: Sourcing and purchasing raw materials.
*   **Assembly Operations**: Processing components using factory machinery.
*   **Quality Inspection**: Testing products to ensure quality compliance.

---

## 5. Organizational Structure
*   **Plant Manager**: Oversees factory operations, safety, and production yields.
*   **Maintenance Operations**: Schedules repairs and maintains factory machinery.
*   **Quality Control**: Runs inspections and audits output batches.
*   **Procurement & Logistics**: Coordinates raw material inflow and shipping.

---

## 6. Enterprise Systems
*   **Manufacturing Execution Systems (MES)**: Controls factory floor operations and tracks active production runs.
*   **Enterprise Resource Planning (ERP)**: Central database tracking financials, purchasing, and logistics.
*   **SCADA (Supervisory Control and Data Acquisition)**: Aggregates real-time telemetry from machine sensors.

---

## 7. KPIs & Metrics
*   **Overall Equipment Effectiveness (OEE)**: Availability x Performance x Quality. Measures machine productivity.
*   **Production Yield**: Percentage of starting materials successfully transformed into finished goods.
*   **Defect Rate**: Percentage of manufactured items rejected during quality inspection.
*   **Downtime**: Duration of unscheduled machine outages.

---

## 8. Regulatory Considerations
*   **ISO Standards (ISO 9001)**: Enforces quality management and manufacturing safety standards.
*   **OSHA Guidelines**: Regulates workplace safety and machine operational protocols.

---

## 9. Business Challenges
*   **Unscheduled Machine Downtime**: Machinery breakdowns halt production, causing lost revenue and high repair costs.
*   **Quality Variations**: Inconsistent raw materials or machine wear lead to product defects and waste.

---

## 10. AI Opportunities

### Predictive Maintenance & Computer Vision Inspections
*   **Predictive Maintenance**: Analyzing vibration and temperature sensor data to identify and resolve machine failures before they occur.
*   **Visual Quality Inspection**: Using computer vision models to identify surface defects on products during assembly.
*   **Production Scheduling**: Optimizing machine scheduling dynamically to maximize OEE.

---

## 11. AI Use Cases
*   **Predictive Maintenance**: Monitoring CNC machine spindle vibration to predict bearing failure.
*   **Quality Control**: Using visual cameras to inspect circuit boards for soldering defects.

---

## 12. Stakeholder Mapping

| Role | Business Goal | Operational Pain Point | AI Opportunity |
|---|---|---|---|
| **Plant Manager** | Maximize OEE, production yields, and safety | Machinery breakdowns halt production | Predictive Maintenance |
| **Quality Lead** | Minimize defect rates and waste | Manual checks miss defects | Visual Quality Inspection |
| **Maintenance Engineer** | Optimize repair schedules and spare parts | Storing excess parts or running out | Spare parts demand forecasting |

---

## 13. Discovery Workshops

### Discovery Questions
*   "What machinery components fail most frequently?" (Identifies predictive maintenance targets).
*   "How are quality inspections currently performed?" (Identifies computer vision opportunities).
*   "What sensor data is captured by your SCADA system?" (Maps data availability).

---

## 14. Case Studies

### Predictive Maintenance Platform at General Electric
General Electric deployed an AI predictive maintenance platform across their manufacturing facilities. By analyzing real-time vibration and temperature data from SCADA systems, they predicted component failures, reducing unscheduled machine downtime by 20% and saving maintenance costs.

---

## 15. Business Value Measurement
*   **Reduction in Unscheduled Downtime**: Track the decrease in machine outage hours.
*   **OEE Improvement**: Measure overall machine productivity gains.
*   **Reduction in Defect Rates**: Track the decrease in quality rejects.

---

## 16. AI FDE Perspective

### Integrating AI with SCADA & MES Systems
As an AI Forward Deployed Engineer (FDE), you often integrate AI models with legacy SCADA systems:
*   **SCADA Integration**: Connect prediction outputs to SCADA systems to trigger alerts or alter machine parameters:
    ```python
    # API update payload config
    # Requests.post("https://core-scada.corp.local/api/alerts/trigger")
    ```
Ensure data transformations are schema-compliant to prevent pipeline write failures.
