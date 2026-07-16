# Practice Tasks: Module 7 - Serverless Deployment Manifests

This document outlines step-by-step tasks to write and inspect KServe deployment manifests.

---

## Task 1: Create KServe Deployment Config
*   **Goal**: Define a serverless predictor service layout.
*   **Step-by-Step Instructions**:
    1. Create a configuration file `kserve_predictor.yaml`:
       ```yaml
       tee /tmp/kserve_predictor.yaml << 'EOF'
       apiVersion: "serving.kserve.io/v1beta1"
       kind: "InferenceService"
       metadata:
         name: "sklearn-iris"
       spec:
         predictor:
           model:
             modelFormat:
               name: sklearn
             storageUri: "gs://kfserving-examples/models/sklearn/1.0/model"
       EOF
       ```
*   **Verification**:
    Verify the yaml resource type matches InferenceService:
    ```bash
    cat /tmp/kserve_predictor.yaml | grep -i "kind: \"InferenceService\""
    ```
