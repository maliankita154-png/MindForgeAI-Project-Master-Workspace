# Deploy AETHERA on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Open [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Select **Create app**, then choose this repository and the branch to deploy.
4. Set **Main file path** to `.github/streamlit_app.py`.
5. Click **Deploy**.

Streamlit Cloud installs the dependencies from the root `requirements.txt` automatically. The included demo CSV files are part of the repository, so no secrets or external database configuration are required.

For a local preview, run:

```powershell
pip install -r requirements.txt
streamlit run .github/streamlit_app.py
```
