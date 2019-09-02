# Data.World and IFTTT Integration (Optional)
This integration is used to fetch recently bookmarked articles from Medium and add them into local dataset.
> This is currently a temporary measure as the Medium API is too limited for such tasks.

### Setup
First of all, You need to do some manual steps.

#### data.world Account Setup
* You need to make an account on [data.world](https://data.world/)
* Create a dataset, name it what you want. <br>
Preferably, "Medium Bookmarks" with stream "medium-bookmarks".

#### IFTTT Account Setup
* Go to [IFTTT](https://ifttt.com/) and make an account
* Activate this applet for your account: [Store Medium bookmarks in a data.world dataset](https://ifttt.com/applets/NNVn2wqv-store-medium-bookmarks-in-a-data-world-dataset) <br>
&nbsp;&nbsp;&nbsp;&nbsp; Note: This is the official applet made by data.world, not made by me.
* Select the relevant `Dataset` and `Stream`

Your Medium now should be connected to data.world through IFTTT. Now, if you add a bookmark in Medium,
it should show up as a `*.jsonl` file in your dataset.




#### Setup your data.world Python Integration
* Open the "**Workplace**" on the dataset
* Find the integrations menu on the top right, click on "**Add More Integrations**"
    - Having Trouble? Use this link: [Python Integration](https://data.world/integrations/python)
* Enable the `python` integration
* Go over to the "**Manage**" tab
* Copy your API Client Token, you'll need it to configure the python Library provided by dataworld. The page should look like the following (As of 06/2019): <br><br>
![](docs/assets/Python_dataworld_API.png)

#### Install the [data.world-py library](https://github.com/datadotworld/data.world-py)
* Run `pip3 install "datadotworld[pandas]"` on your terminal ("" are only required if you are using zsh shell rather than bash shell)
* Now, you need to configure the library to use **your** dataworld dataset using the API client Token
    - You can either run `dw configure` on your terminal and paste the API Token
    - Alternatively, tokens can be provided via the DW_AUTH_TOKEN environment variable. On MacOS or Unix machines, run (replacing \<YOUR_TOKEN> below with the token obtained earlier): <br>
    `export DW_AUTH_TOKEN=<YOUR_TOKEN>`
