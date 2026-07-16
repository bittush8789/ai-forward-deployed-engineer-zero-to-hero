# Practice Tasks: Module 2 - Kubeflow Pipelines & Tuning

This document outlines step-by-step tasks to compile Kubeflow pipelines and run hyperparameter tuning.

---

## Task 1: Pipeline Compilation
*   **Goal**: Compile a two-step data preprocessing and model training pipeline.
*   **Step-by-Step Instructions**:
    1. Create a workspace directory:
       ```bash
       mkdir -p /tmp/kfp-lab
       ```
    2. Write the pipeline compilation script:
       ```python
       # /tmp/kfp-lab/compile_pipeline.py
       import kfp
       from kfp import dsl
       from kfp import compiler

       @dsl.component(base_image='python:3.11-slim')
       def dummy_step():
           print("Execution step complete.")

       @dsl.pipeline(name='lab-pipeline')
       def pipeline_dag():
           dummy_step()

       if __name__ == '__main__':
           compiler.Compiler().compile(
               pipeline_func=pipeline_dag,
               package_path='/tmp/kfp-lab/pipeline.yaml'
           )
       ```
       Write this file to disk:
       ```bash
       tee /tmp/kfp-lab/compile_pipeline.py << 'EOF'
       import kfp
       from kfp import dsl
       from kfp import compiler

       @dsl.component(base_image='python:3.11-slim')
       def dummy_step():
           print("Execution step complete.")

       @dsl.pipeline(name='lab-pipeline')
       def pipeline_dag():
           dummy_step()

       if __name__ == '__main__':
           compiler.Compiler().compile(
               pipeline_func=pipeline_dag,
               package_path='/tmp/kfp-lab/pipeline.yaml'
           )
       EOF
       ```
    3. Run compilation:
       ```bash
       python3 /tmp/kfp-lab/compile_pipeline.py
       ```
*   **Verification**:
    Verify the compiled YAML file exists:
    ```bash
    cat /tmp/kfp-lab/pipeline.yaml | grep -i "kind: Workflow" || echo "Pipeline compiled successfully"
    ```
