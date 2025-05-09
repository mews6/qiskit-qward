import plotly.express as px
import pandas as pd

def execution_result_histogram(jobs):
    df = pd.DataFrame({"Job Batch":[],
                       "Result":[],
                       "Count":[]})

    for i, job in enumerate(jobs):
        result = job.result()
        counts = result.get_counts()

        results = {}
        print(counts)
        for j in counts:
            if j not in results.keys():
                results[j] = 1
            else:
                results[j] += 1
        for j in results.keys():

            batch = pd.DataFrame({"Job Batch":[f"Job Batch {i}"],
                       "Result":[j],
                       "Count":[results[j]]})
            df = pd.concat([df, batch])

    fig = px.histogram(data_frame=df, x="Result", y="Count")
    fig.show()