# @Author  :_kerman jt
# @Time    : 19-12-1 下午3:34

import os
from blog.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)

