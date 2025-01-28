from supabase import create_client, Client

# Supabase Konfiguration
SUPABASE_URL = "https://aws-supabase-u31663.vm.elestio.app/"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYW5vbiIsImlzcyI6InN1cGFiYXNlIiwiaWF0IjoxNzM3NzI5OTIzLCJleHAiOjIwNTMwODk5MjN9.L-oUAxVZHbi2QzmAy0mgFV9AA0Wql1wLkW1kYUcGmO0"

# Webhook URLs
WEBHOOK_URL_RUDI = "https://n8ntb.sts.support/webhook/9ba11544-5c4e-4f91-818a-08a4ecb596c5"
WEBHOOK_URL_TEST = "https://n8ntb.sts.support/webhook/2c474e5f-0350-4bdf-b0c4-dbf73f919659"

# Supabase Client initialisieren
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)