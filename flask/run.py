from myproject import app


if __name__ == '__main__':
    app.run(host='0.0.0.0')

from myproject.reddit import ThreadManager
import myproject.views
manager = ThreadManager()