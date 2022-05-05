import os
try:
  from google.analytics.data_v1beta import BetaAnalyticsDataClient
  from google.analytics.data_v1beta.types import DateRange
  from google.analytics.data_v1beta.types import Dimension
  from google.analytics.data_v1beta.types import Metric
  from google.analytics.data_v1beta.types import RunReportRequest
except:
  print("Error importing GA packages. Will attempt to install using colab syntax. This will restart the runtime.")
  !pip install google-analytics-data
  os.kill(os.getpid(), 9)

# Utility function to convert to dataframe
def ga4_response_to_df(response):
    dim_len = len(response.dimension_headers)
    metric_len = len(response.metric_headers)
    all_data = []
    for row in response.rows:
        row_data = {}
        for i in range(0, dim_len):
            row_data.update({response.dimension_headers[i].name: row.dimension_values[i].value})
        for i in range(0, metric_len):
            row_data.update({response.metric_headers[i].name: row.metric_values[i].value})
        all_data.append(row_data)
    df = pd.DataFrame(all_data)
    return df
  
# Define default report dimensions and metrics
defDims = [Dimension(name="customEvent:ga_session_id"),
                Dimension(name="customEvent:timestamp"),
                Dimension(name="eventName"),
                Dimension(name="pageTitle"),
                Dimension(name="customEvent:text")]
defMets = [Metric(name="eventCount")]

# Function to pull report and return dataFrame
def sample_run_report(property_id="MISSING", startDate="yesterday", endDate="yesterday", dims=defDims, mets=defMets, creds=""):
    # Set environment variables
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds
    # Using a default constructor instructs the client to use the credentials
    # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=dims,
        metrics=mets,
        date_ranges=[DateRange(start_date=startDate, end_date=endDate)],
    )
    response = client.run_report(request)
    # Return report as dataFrame
    return ga4_response_to_df(response)