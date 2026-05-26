---
title: "Billit API Source Docs - How Do I Get Started With Curl"
updated: 2026-05-26
---

# How do i get started with Curl?\n\n_In this article I will explain how to get started with Curl and demonstrate some example API calls with extra information._

# Getting started   [Skip link to Getting started](https://docs.billit.be/docs/curl\#getting-started)

Curl is a command-line utility, this means it is recommended that you experiment with API calls on Sandbox, as most likely your local will be blocked due to having an invalid certificate.

Curl is installed by default on most Linux and macOS distributions.

If your PC has Windows then there are 3 options to start with Curl:

1. Installed by default on Windows 10, version 1803 or later.

2. If you have [Git for Windows](https://gitforwindows.org/) installed (if you downloaded Git from [git-scm.com](https://git-scm.com/), the answer is yes), you have `curl.exe` under:



Text





```\1

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

# Options to expand your Curl calls   [Skip link to Options to expand your Curl calls](https://docs.billit.be/docs/curl\#options-to-expand-your-curl-calls)

In curl there are several options you can add to your request to change the requests behaviour.

Standard curl syntax looks like this:

Bash

```\1

 curl [options] [URL...]

```

The possible options are:

- `-X`, `--request` \- The HTTP method to be used.
- `-i`, `--include` \- Include the response headers.
- `-d`, `--data` \- The data to be sent.
- `-H`, `--header` \- Additional header to be sent.
- `-v`, \- This will make the commands provide helpful information such as the resolved IP address, the port and the headers.
- `-o`, `name.extension` \- By default curl outputs the response to standard output, we can provide an output option to change this.

# Example API Calls   [Skip link to Example API Calls](https://docs.billit.be/docs/curl\#example-api-calls)

1. GET Order



Bash





```\1

curl -X GET https://api.sandbox.billit.be/v1/order/{OrderId} --header "Content-Type:application/json" --header "apikey:{MyApiKey}" --header "partyID:{MyPartyID}" --header "Accept: application/json"

```

2. GET List of Orders with Filter



Bash





```\1

curl -X GET --url "https://api.sandbox.billit.be/v1/orders?%24filter=OrderNumber%20eq%20%272022%2FTEST06%27" --header "Content-Type:application/json" --header "apikey:{MyApiKey}" --header "partyID:{MyPartyID}" --header "Accept: application/json"

```





Additionally you could make this more readable by making the OData plain text, both will work.


Make note that it is possible you will have to escape the dollarsign "\\$" for Linux and similar environments to prevent incorrect encoding.



Bash





```\1

curl -G https://api.sandbox.billit.be/v1/orders --data-urlencode "$filter=OrderNumber eq '2022/TEST06'" --header "Content-Type:application/json" --header "apikey:{MyApiKey}" --header "partyID:{MyPartyID}" --header "Accept: application/json"

```

3. POST Order



Bash





```\1

curl -d "{\"OrderType\":\"Invoice\",\"OrderDirection\":\"Income\",\"OrderDate\":\"2022-08-17\",\"ExpiryDate\":\"2022-09-24\",\"OrderLines\": [{\"Quantity\":1,\"Description\":\"Test Item 1\",\"VATPercentage\":0.00,\"UnitPriceExcl\":6.0000},{\"Quantity\":1,\"Description\":\"Test Item 1\",\"VATPercentage\":0.00,\"UnitPriceExcl\":3.5000}],\"Customer\":{\"Name\":\"Billit3\",\"VATNumber\":\"BE0000089971\",\"PartyType\":\"Customer\"}}"  -H "Content-Type: application/json" https://api.sandbox.billit.be/v1/orders/ --header "apikey:{MyApiKey}" --header "partyID:{MyPartyID}" --header "Accept: application/json"

```


Updated23 days ago

* * *

Did this page help you?

Yes

No