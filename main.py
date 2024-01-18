from website import create_app
#from livereload import Server

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
   # server = Server(app.wsgi_app) #próba automatycznej aktualizacji
   # server.serve()
    
