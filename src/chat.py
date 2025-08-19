#!/usr/bin/env python3

#    Ask ChatGPT 4.1 about a pdf in a CLI
#    Copyright (C) 2025  Vetle Tjora

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

# imports
from colorama import Fore, Style, init
from sys import argv
import re
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder, FileSearchTool, FilePurpose

def remove_citations(text: str) -> str:
    return re.sub("【.*?】", "", text).strip()

if __name__ == "__main__":
    # initialise colorama:
    init(autoreset=True)

    # set the model name
    model_name = "gpt-4.1-nano"
    # give the name a colour in the CLI
    ui_name = f"{Fore.GREEN}{re.sub("-", " ", model_name)}{Style.RESET_ALL}"

    # get the pdf by argument or prompt
    try:
        file = argv[1]
        print(f"{ui_name}: Welcome! Ask any question about {file} to begin")
        print("")
    except IndexError:
        print("{ui_name}: Welcome! What pdf should I answer questions about?")
        print("")
        file = input(f"{Fore.BLUE}you{Style.RESET_ALL}: ")
        print("")
        print(f"{ui_name}: Ask any question about {file} to begin")
        print("")

    # get user input
    user_input = input(f"{Fore.BLUE}you{Style.RESET_ALL}: ")
    print("")

    # connect to Azure AI project
    project = AIProjectClient(
        endpoint="https://vetle-4221-resource.services.ai.azure.com/api/projects/vetle-4221",
        credential=DefaultAzureCredential(),
    )

    # create vector store
    file = project.agents.files.upload(file_path=file, purpose=FilePurpose.AGENTS)
    vector_store = project.agents.vector_stores.create_and_poll(
        file_ids=[file.id], name="my_file"
    )

    # create file search toool and agent
    file_search = FileSearchTool(vector_store_ids=[vector_store.id])
    agent = project.agents.create_agent(
        model="gpt-4.1-nano",
        name=model_name,
        instructions="You are a helpful assistant answering questions regarding the PDF. Keep the answers short and concise. Never give follow-up questions.",
        tools=file_search.definitions,
        tool_resources=file_search.resources,
    )

    # start user question/AI answer loop until user types 'exit' or similar
    while user_input.lower() not in ("quit", "exit", "cancel"):

        # NOTE: we create a new thread inside the loop to minimise token usage.
        #       This will of course make the chat unable to answer follow-ups.

        # create thread and process user input
        thread = project.agents.threads.create()
        project.agents.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input,
        )
        run = project.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)

        # handle run errors
        if run.status == "failed":
            print(f"{Fore.RED}.run failed{Style.RESET_ALL}: {run.last_error}")

        # print thread messages
        messages = project.agents.messages.list(
            thread_id=thread.id, order=ListSortOrder.ASCENDING
        )

        # set bot name
        role = f"{Fore.GREEN}{ui_name}{Style.RESET_ALL}: "

        for message in messages:
            if message.run_id == run.id and message.text_messages:
                raw_text = message.text_messages[-1].text.value
                print(f"{role}{remove_citations(raw_text)}")
                print("")
                role = "" # remove bot name to make chat cleaner

        # get new user imput
        user_input = input(f"{Fore.BLUE}you{Style.RESET_ALL}: ")
        print("")

    # cleanup
    print("exiting...")
    project.agents.vector_stores.delete(vector_store.id)
    project.agents.files.delete(file_id=file.id)
    project.agents.delete_agent(agent.id)
