# Day32 RNN Apps

This folder contains two separate Streamlit deployment-ready apps:

- sms_app/ - SMS spam detection with an RNN
- shakespeare_app/ - Shakespeare text generation with a character-level RNN

## Deploy separately

### SMS app
```bash
cd sms_app
streamlit run app.py
```

### Shakespeare app
```bash
cd shakespeare_app
streamlit run app.py
```

## GitHub-ready notes
- Each app folder is self-contained.
- Each folder includes its own requirements.txt.
- Each folder includes the required model/data files needed to run the app.
