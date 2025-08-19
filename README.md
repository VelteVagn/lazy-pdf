# PDF Chat

Ask ChatGPT 4.1 nano about a pdf of your choice. 

## Usage

Clone the repository
```
git clone https://github.com/VelteVagn/this-repo.git
cd this-repo
```

Create and activate a virtual environment:
Unix:
```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:
```cmd
python -m venv venv
source venv\Scripts\activate.bat
```

```powershell
python -m venv venv
source venv\Scripts\activate.ps1
```

Windows:
```cmd
python -m venv venv
source venv\Scripts\activate.bat
```

```powershell
python -m venv venv
source venv\Scripts\activate.ps1
```

Install dependencies:
```
pip install -r requirements.txt
```

Run the program:
```
python src/chat.py path/to/pdf
```

If you omit the pdf like so
```
python src/chat.py
```
you will be prompted to give the path to the pdf when the program runs.

## License

This project is licensed under the [GNU Affero General Public License (AGPL)](COPYING).

## Notes

This prgram connects to ChatGPT via Microsoft Azure which means a couple of things:
1. To use it, you'll need a Microsoft Azure account, and either [ask me](#contact) for the proper permissions or substitute the endpoint with your own. 
2. Since I merely have a free subscription, regardless of permissions, the program will stop working in not too long when my free tokens expire.
3. To not waste tokens, the program is made to minimise token use as much as possible, which necessarily weakens the functionality. 

This program is based on code from Microsoft's [Quickstart: Get started with Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/quickstarts/get-started-code?tabs=python&pivots=fdp-project). 

## Contact
vetle@tjora.net
