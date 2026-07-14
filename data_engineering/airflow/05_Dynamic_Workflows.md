# Module 3.5: Dynamic Workflows

Welcome to **Dynamic Workflows**. Hardcoding tasks is fine for 5 tables, but what if you need to ingest 500 tables? Writing 500 `BashOperators` by hand is not scalable. Because Airflow DAGs are just Python code, you can generate tasks and DAGs dynamically at runtime.

---

## 1. Detailed Theory

### Dynamic DAG Generation
You can use Python loops (`for table in table_list:`) at the top level of your DAG file to dynamically generate tasks.
- **Warning**: Code at the top level of a DAG file is parsed by the scheduler every 30 seconds. If your loop pulls the `table_list` from a slow database query, you will crash the Airflow scheduler.

### Dynamic Task Mapping
Introduced in Airflow 2.3, this is a safer, built-in way to generate tasks at runtime *without* crashing the scheduler. 
Instead of a `for` loop, you use `.expand()`. If a previous task returns a list of 5 files, `.expand()` will dynamically create 5 parallel tasks to process those files.

### Task Groups
When you have 50 tasks in a DAG, the Web UI becomes an unreadable mess of lines. **TaskGroups** allow you to visually group related tasks together in the UI (e.g., grouping all `extract_*` tasks into one expandable box).

### Modular DAG Design
Instead of one massive 2,000-line DAG, you should break pipelines into smaller, reusable components.
- **TriggerDagRunOperator**: Allows DAG A to trigger DAG B. (e.g., A daily ingestion DAG triggers a separate model retraining DAG upon success).

---

## 2. Architecture Diagram: Dynamic Task Mapping

```mermaid
flowchart TD
    subgraph "Airflow Dynamic Task Mapping"
        GetList[PythonOperator\nReturns: ['file1.csv', 'file2.csv', 'file3.csv']]
        
        GetList --> |Outputs List| MapLogic{Airflow .expand()}
        
        MapLogic --> TaskA[Process file1.csv]
        MapLogic --> TaskB[Process file2.csv]
        MapLogic --> TaskC[Process file3.csv]
        
        TaskA --> Merge[Merge Results]
        TaskB --> Merge
        TaskC --> Merge
    end
```

---

## 3. Production Use Cases

1. **Multi-Tenant Ingestion Pipeline**: You have a SaaS platform with 50 enterprise clients. You don't want 50 different DAGs. You write one DAG that queries a configuration database for active clients, uses Dynamic Task Mapping, and spins up parallel ingestion tasks for however many clients are active that day.
2. **Chunking Massive Documents for RAG**: An S3 bucket receives 1,000 PDFs. Task 1 lists all the PDFs. Task 2 uses `.expand()` to dynamically map 1,000 parallel chunking tasks to a Kubernetes cluster to process them in minutes.

---

## 4. Real Company Examples

- **Astronomer**: Strongly advocates for Dynamic Task Mapping over traditional `for` loops in top-level code, writing extensive documentation on how to build scalable pipelines that adapt to varying data volumes automatically.

---

## 5. Coding Examples

### Dynamic Task Mapping (Airflow 2.3+)

```python
from datetime import datetime
from airflow.decorators import dag, task

@dag(start_date=datetime(2023, 1, 1), schedule_interval='@daily', catchup=False)
def dynamic_mapping_dag():

    # 1. Task that returns a list
    @task
    def get_files():
        return ['data_2023_01.csv', 'data_2023_02.csv', 'data_2023_03.csv']

    # 2. Task that processes a SINGLE file
    @task
    def process_file(filename: str):
        print(f"Processing {filename}...")
        return f"Done with {filename}"

    # 3. Task that summarizes the results
    @task
    def summarize(results: list):
        print(f"Total processed: {len(results)}")

    # 4. Define the flow using .expand()
    files_list = get_files()
    
    # This dynamically creates 3 parallel 'process_file' tasks
    processed_results = process_file.expand(filename=files_list)
    
    summarize(processed_results)

# Instantiate the DAG
dag_instance = dynamic_mapping_dag()
```

---

## 6. Hands-on Labs

**Lab: Task Groups**
**Objective**: Clean up a messy DAG UI.
**Instructions**:
Write the Python syntax to create a `TaskGroup` called `data_extraction` and place two dummy tasks inside it. (Hint: Use `with TaskGroup(group_id='data_extraction') as extract_group:`).

---

## 7. Assignments

**Assignment: The Top-Level Code Danger**
You wrote a DAG that uses a `for` loop to dynamically generate a task for every row in a massive Postgres table. You put the `psycopg2` database connection and the `SELECT * FROM massive_table` query directly in the DAG file, outside of any operator. 
Explain exactly what will happen to the Airflow Scheduler when you deploy this file.

---

## 8. Interview Questions

1. **What is Dynamic Task Mapping in Airflow?**
   *Answer Hint: A feature (using `.expand()`) that allows Airflow to dynamically create tasks at runtime based on the output list of a previous task, avoiding the dangers of executing top-level code in the DAG file.*
2. **Why would you use a `TriggerDagRunOperator`?**
   *Answer Hint: To decouple complex pipelines. Instead of a monolithic DAG that is impossible to debug, you can have a "Data Ingestion" DAG trigger a "Model Training" DAG only when ingestion completes successfully.*

---

## 9. Best Practices (FDE Standards)

- **Use the Taskflow API (`@task`)**: For Python-heavy DAGs, prefer the modern Taskflow API decorators over manually instantiating `PythonOperators`. It handles passing XComs automatically between tasks.
- **Externalize Configuration**: If your dynamic DAG depends on a list of 50 tables, store that list in a YAML file or an Airflow Variable, don't hardcode the list in the Python script.

---

## 10. Common Mistakes

- **Expanding Too Many Tasks**: If Task 1 returns a list of 100,000 files, and you use `.expand()` on Task 2, Airflow will try to create 100,000 tasks in the metadata database instantly, likely crashing it. For massive numbers, batch the files into lists of 1,000 before expanding.
