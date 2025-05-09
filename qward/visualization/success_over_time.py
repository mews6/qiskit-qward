import plotly.express as px
import pandas as pd

def success_over_time_lines(jobs, n):
    df = pd.DataFrame({"Batch":[],
                       "Success Rate":[]})
    for i, job in enumerate(jobs):
        
        result = job.result()
        counts = result.get_counts()
        total_shots = sum(counts.values())
        successful_shots = counts.get('0'*n, 0)
        success_rate = successful_shots / total_shots if total_shots > 0 else 0.0

        batch = pd.DataFrame(
            {
                "Batch":[f"Batch Job {i+1}"],
                "Success Rate":[success_rate]
            })
        df.append(batch)
    
    fig = px.line(df, x="Batch", y="Success Rate", title=f'Success rate of {i} batches')
    fig.show()