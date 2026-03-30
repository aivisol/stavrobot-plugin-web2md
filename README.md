# stavrobot-plugin-web2md

Converts any webpage to clean Markdown using the [Apify](https://apify.com/) `extremescrapes/webpage-to-markdown` actor.

## What it does

Provide a URL and get back the page content as Markdown — useful for reading articles, documentation, or any web content in a clean, LLM-friendly format.

## Installation

Tell Stavrobot:

> Install the plugin from https://github.com/aivisol/stavrobot-plugin-web2md

Then configure your Apify API token:

> Configure the web2md plugin with my Apify token: `<your token>`

Get your token from [https://console.apify.com/account/integrations](https://console.apify.com/account/integrations). A free Apify account includes enough credits to run this actor.

## Usage

> Convert https://example.com to Markdown

The tool launches an Apify actor run and polls for the result asynchronously — the response arrives once the scrape is complete (typically within 30–60 seconds).
