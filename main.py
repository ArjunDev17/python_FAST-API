from uvicorn import run
def main():
    host = '0.0.0.0'  # Host IP address
    port = 8086  # Port number
    app_module = 'app.main:app'  # Module and app name

    run(app_module, host=host, port=port, reload=True)

if __name__ == '__main__':
    main()

# # create requirements.txt
# # pip freeze > requirements.txt