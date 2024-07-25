# *-* coding: utf-8 *-*
# main.py

import uvicorn, ssl


# Método de inicio para la aplicación usando uvicorn y con SSL (privkey.pem & cert.pem)
if __name__ == "__main__":
  context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
  context.load_cert_chain(certfile="cert.pem", keyfile="privkey.pem")
  uvicorn.run("app.api:app", host="0.0.0.0", port=8081, reload=True, ssl_keyfile="privkey.pem", ssl_certfile="cert.pem")