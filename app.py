from flight_club import get_app
import os

if __name__ == "__main__":
    app = get_app()
    # port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0")
