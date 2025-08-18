#!/usr/bin/env python3
from sys import argv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder, FileSearchTool, FilePurpose

try:
    file = argv[1]
    print(f"Welcome! Ask any question about {file} to begin")
except IndexError:
    print("Welcome! What pdf should I answer questions about?")
    file = input()
    print(f"Ask any question about {file} to begin")

user_input = input()

project = AIProjectClient(
    endpoint="https://vetle-4221-resource.services.ai.azure.com/api/projects/vetle-4221",
    credential=DefaultAzureCredential(),
)

# create vector store
file = project.agents.files.upload(file_path=file, purpose=FilePurpose.AGENTS)
vector_store = project.agents.vector_stores.create_and_poll(file_ids=[file.id], name="my_file")

file_search = FileSearchTool(vector_store_ids=[vector_store.id])
agent = project.agents.create_agent(
    model="gpt-4.1-nano",
    name="gpt-4.1-nano",
    instructions="You are a helpful assistant answering questions regarding the PDF.",
    tools=file_search.definitions,
    tool_resources=file_search.resources,
)

while user_input.lower() not in ('quit', 'exit', 'cancel'):
    thread = project.agents.threads.create()
    project.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input,
    )
    run = project.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)

    if run.status=="failed":
        print(f"run failed: {run.last_error}")

    messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    for message in messages:
        if message.run_id == run.id and message.text_messages:
            print(f"{message.role}: {message.text_messages[-1].text.value}")
    user_input = input()

print("exiting...")
project.agents.vector_stores.delete(vector_store.id)
project.agents.files.delete(file_id=file.id)
project.agents.delete_agent(agent.id)

