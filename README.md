# booking API APps




- ローカルでfastapiのAPIサーバーを立ち上げる
`uvicorn src.sql_app.main:app --reload`

- ローカルでフロントを立ち上げる
`streamlit run src/app.py`


# Obs Vercel Deploy

Vercelでのリリースにおける注意事項
- `requirements.loc`はNG。`requirements.txt`にする必要がある


`vercel cli`でのリリース
- `vercel login`
- `vercel .`
- `vercel --prod`
