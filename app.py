# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 13:59:04 2019

@author: wlgn567@naver.com
"""

from flask import Flask, jsonify, request, abort
import psutil
import os
import random, string

# 키 생성 및 비교를 위한 클래스
class ServerKey():
    # 객체 변수
    SERVER_KEY = None
    
    # 생성자
    def __init__(self):
        # 객체 생성 시, 키를 생성한다.
        self.make_key()
    
    # 키 생성 함수
    def make_key(self):
        # 현재폴더 하위에 .key 파일이 존재하는지 확인.
        if(os.path.isfile('./.key')):
            # 존재할 경우 읽어서 SERVER_KEY 변수에 입력.
            with open("./.key", 'r') as f:
                self.SERVER_KEY = f.read()
        else:
            # 존재하지 않을 경우 SERVER_KEY 새로 생성 후, .key 파일 생성
            with open("./.key", 'w') as f:
                letters = string.ascii_uppercase + string.digits
                self.SERVER_KEY = "".join(random.choices(letters, k=20))
                print("MAKE KEY : {}".format(self.SERVER_KEY))
                f.write(self.SERVER_KEY)
                
    # key 비교 함수
    def check_key(self, request):
        print(request.form.get('key'))
        print(request.args.get('key')) 
        key = request.args.get('key')
        
        if(not(self.SERVER_KEY == key)):
            return False
        
        return True
    

# flask App 생성
app = Flask(__name__)
# key 클래스 생성
key = ServerKey()


# 시스템 상태 체크 메소드
@app.route('/check', methods=['POST'])
def check():
    # 만약 key가 다르다면 
    if(not(key.check_key(request))):
        abort(401)
    
    mem = psutil.virtual_memory()
    status = {
            'CPU_PERCENT' : psutil.cpu_percent(),
            'MEM_TOTAL': "{:.2f}".format(mem.total*0.001*0.001),
            'MEM_USED': "{:.2f}".format(mem.used*0.001*0.001),
            'MEM_FREE': "{:.2f}".format(mem.free*0.001*0.001),
    }
    
    return jsonify(status)
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
