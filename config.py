from supabase import create_client, Client

# Supabase Konfiguration
SUPABASE_URL = "https://aws-supabase-u31663.vm.elestio.app/"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYW5vbiIsImlzcyI6InN1cGFiYXNlIiwiaWF0IjoxNzM3NzI5OTIzLCJleHAiOjIwNTMwODk5MjN9.L-oUAxVZHbi2QzmAy0mgFV9AA0Wql1wLkW1kYUcGmO0"

# Webhook URLs
WEBHOOK_URL_RUDI = "https://n8ntb.sts.support/webhook/9ba11544-5c4e-4f91-818a-08a4ecb596c5"
WEBHOOK_URL_PERPLEXITY = "https://n8ntb.sts.support/webhook/fcbaa65b-1386-4ceb-83a2-9cabddb7ee2d"
WEBHOOK_URL_CHATGPT = "https://n8ntb.sts.support/webhook/15a9f295-cc12-4bb3-9b1b-adc3cb0e9d5a"
WEBHOOK_URL_MISTRAL = "https://n8ntb.sts.support/webhook/a6940db2-b459-488f-ab7a-370da816c841"
WEBHOOK_URL_DEEPSEEK = "https://n8ntb.sts.support/webhook/754e182c-25e0-4056-afa9-0bc8552ff977"
WEBHOOK_URL_GEMINI_FLASH = "https://n8ntb.sts.support/webhook/aaa7b1dc-d574-446a-8a57-772e8aa9ace0"
WEBHOOK_URL_GEMINI_THINKING = "https://n8ntb.sts.support/webhook/e4ab4a4d-ae20-4703-87d9-20ad72c51cd1"
WEBHOOK_URL_CLAUDE = "https://n8ntb.sts.support/webhook/4f91274f-cd38-45da-9d24-f4ecfec6d1f7"

# Supabase Client initialisieren
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)