from flaskblog import create_app 

app = create_app()  # pass in null to use default Config. 

# Run app 
if __name__ == '__main__':
    app.run(debug=True)


