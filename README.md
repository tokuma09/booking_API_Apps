# vercel_sample

Vercelでのリリースにおける注意事項
- requirements.locはNG。requirements.txtにする必要がある


vercel cliでのリリース
- vercel login
- vercel .
- vercel --prod


ローカルでfastapiのAPIサーバーを立ち上げる
- uvicorn src.main:app --reload

ローカルでフロントを立ち上げる
- streamlit run src/app.py
