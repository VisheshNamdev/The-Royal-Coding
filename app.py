from website import create_app

# Create the Flask app instance
app = create_app()

if __name__ == "__main__":
    # Run the Flask app with debug mode enabled
    app.run(host='0.0.0.0', debug=False)
