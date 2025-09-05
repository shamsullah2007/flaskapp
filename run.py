from app import app



if __name__ == "__main__":
    # with app.app_context():  # push app context
    #     db.create_all()     # creates tables in mydatabase.db
    app.run(debug=True)