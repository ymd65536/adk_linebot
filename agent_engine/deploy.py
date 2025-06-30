import os
from get_weather_agent_ae.agent import root_agent

import vertexai
from vertexai import agent_engines
from vertexai.preview import reasoning_engines

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
STAGING_BUCKET = os.getenv("STAGING_BUCKET", "your-staging-bucket")


vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)

adk_app = reasoning_engines.AdkApp(
    agent=root_agent,
    enable_tracing=False,
)

remote_agent = agent_engines.create(
    adk_app,
    display_name="Get Weather Agent",
    requirements=[
        "google-adk==1.3.0",
        "google-genai==1.17.0",
        "google-cloud-aiplatform[adk,agent-engines]==1.95.1",
    ],
    extra_packages=["get_weather_agent"]
)
