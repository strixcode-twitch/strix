# Stupid VSCode thingy
import multiprocessing
multiprocessing.set_start_method('spawn', True)

from Strix import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, auto_reload=False)
