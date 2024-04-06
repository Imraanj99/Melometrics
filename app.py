from website import create_app

app = create_app()

if __name__ == '__main__':
    print(app.static_folder)
    app.run(debug=True, port=5001)
