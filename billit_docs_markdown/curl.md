---
title: "Curl Command Line interface"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/curl"
source_slug: "curl"
category: "reference-errors"
topics:
  - reference
  - errors
  - curl
  - command
  - line
  - interface
---

# Why CURL

Some (older) sending applications do not support API. Then Curl can be a command line based alternative, still using the some values and logic as the API

# Getting started

Curl is a command-line utility, this means it is recommended that you experiment with API calls on Sandbox, as most likely your local will be blocked due to having an invalid certificate.

Curl is installed by default on most Linux and macOS distributions.

If your PC has Windows then there are 3 options to start with Curl:

1. Installed by default on Windows 10, version 1803 or later.

2. If you have [Git for Windows](https://gitforwindows.org/) installed (if you downloaded Git from [git-scm.com](https://git-scm.com/), the answer is yes), you have `curl.exe` under:

Text

```text
    C:\Program Files\Git\mingw64\bin\
```

Simply add the above path to `PATH`.

3. Download the Curl package you desire from [here](https://curl.haxx.se/windows/), these are the official Windows builds provided by the [curl-for-win](https://github.com/curl/curl-for-win) project.

Find `curl.exe` within your downloaded package, it's probably under `bin\`.

Pick a location on your hard drive that will serve as a permanent home for curl.

Place `curl.exe` under that folder. And **NEVER** move the folder or its contents.

Next, you'll want to make curl available anywhere from the command line. To do this, add the folder to `PATH`, like this:
1. Start typing "environment" in the Windows 10 start menu.
2. Choose **Edit the system environment variables**.
3. Click the **Environment Variables** button at the bottom.
4. Select the "Path" variable under "System variables" (the lower box). Click the **Edit** button.
5. Click the **Add** button and paste in the folder path where `curl.exe` lives.
6. Click **OK** as needed. Newly opened console windows will have the new `PATH`.

# Options to expand your Curl calls

In curl there are several options you can add to your request to change the requests behaviour.

Standard curl syntax looks like this:

Bash

```shell
 curl [options] [URL...]
```

The possible options are:

- `-X`, `--request` \- The HTTP method to be used.
- `-i`, `--include` \- Include the response headers.
- `-d`, `--data` \- The data to be sent.
- `-H`, `--header` \- Additional header to be sent.
- `-v`, \- This will make the commands provide helpful information such as the resolved IP address, the port and the headers.
- `-o`, `name.extension` \- By default curl outputs the response to standard output, we can provide an output option to change this.

# Example API Calls

1. GET Order

Bash

```shell
curl -X GET https://api.sandbox.billit.be/v1/order/{OrderId} --header "Content-Type:application/json" --header "apikey:{MyApiKey}" --header "partyID:{MyPartyID}" --header "Accept: application/json"
```

2. GET List of Orders with Filter

Bash

```shell
curl -X GET --url "https://api.sandbox.billit.be/v1/orders?%24filter=OrderNumber%20eq%20%272022%2FTEST06%27" --header "Content-Type:application/json" --header "apikey:{MyApiKey}" --header "partyID:{MyPartyID}" --header "Accept: application/json"
```

Additionally you could make this more readable by making the OData plain text, both will work.

Make note that it is possible you will have to escape the dollarsign "$" for Linux and similar environments to prevent incorrect encoding.

Bash

```shell
curl -G https://api.sandbox.billit.be/v1/orders --data-urlencode "$filter=OrderNumber eq '2022/TEST06'" --header "Content-Type:application/json" --header "apikey:{MyApiKey}" --header "partyID:{MyPartyID}" --header "Accept: application/json"
```

3. POST Order

Bash

```shell
curl -d "{\"OrderType\":\"Invoice\",\"OrderDirection\":\"Income\",\"OrderDate\":\"2022-08-17\",\"ExpiryDate\":\"2022-09-24\",\"OrderLines\": [{\"Quantity\":1,\"Description\":\"Test Item 1\",\"VATPercentage\":0.00,\"UnitPriceExcl\":6.0000},{\"Quantity\":1,\"Description\":\"Test Item 1\",\"VATPercentage\":0.00,\"UnitPriceExcl\":3.5000}],\"Customer\":{\"Name\":\"Billit3\",\"VATNumber\":\"BE0000089971\",\"PartyType\":\"Customer\"}}"  -H "Content-Type: application/json" https://api.sandbox.billit.be/v1/orders/ --header "apikey:{MyApiKey}" --header "partyID:{MyPartyID}" --header "Accept: application/json"
```
