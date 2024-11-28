Simple client for pulling some baseline OTF data. Depends on the [otf-api package](https://otf-api.readthedocs.io/en/stable/). This populates data in the format expected by a [Google sheet shared](https://docs.google.com/spreadsheets/d/1DUj1Lx660Dp0Q6nPECQqu-CYgEEpmX99UzAHzgW1er4/edit?fbclid=IwZXh0bgNhZW0CMTEAAR1BOO7bJC2IjEeDyKOwVSrqlpLseWK6Kno-0GlhdGOz4xWO3Jpb50lTJ3U_aem_8iTVbHtrGHbxaA_axH4rBA&gid=0#gid=0) by a fellow OTF member. This sheet calculates some useful visualizations of your performance history.

## Running this script
Requires minimum of Python 3.12 to run as otf-api requires this.

Copy the env.sample file to a file that ends in `.env` as the script loads through dotenv module any env files in the folder. Populate with your user credentials used for the OTF App, and pass that file as a parameter to the script.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python generate_otfdata.py
```

Disclaimer:
This project is in no way affiliated with OrangeTheory Fitness.
