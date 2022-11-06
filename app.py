# URL: https://sctube.run.goorm.io/
from flask import Flask, redirect, request, render_template, jsonify, send_file, after_this_request
from src import ytdl
from glob import glob
from sys import stdin, argv
from time import strftime, localtime

import os

app = Flask(__name__)

"""
main page
input you want video url
"""
@app.route("/")
def main():
	print(f"main page")
	return render_template("main.html")

@app.route("/video")
def video():
	print(f"video page")
	return render_template("video.html")

@app.route("/audio_only", methods=["GET","POST"])
def audio_only():
    print("audio file page")
    return render_template("audio_only.html")

"""
download page
loading window
server local download and send file page
"""
@app.route("/downloading", methods=["post"])
def downloading():
	hash = request.form["hash"]
	nextUrl = request.form["nextUrl"]
	print(f"downloading page")
	print(f"hash: {hash}")
	print(f"next URL: {nextUrl}")
    
	now_date = strftime('%Y. %m. %d. %H:%M:%S(%a) KST')
    
	with open("log/download_list.csv",'a') as f:
		f.write(f"{now_date}, {hash}\n")
    
	return render_template("download.html", hash=hash, nextUrl=nextUrl)

"""
sld = server local download
server local download on video
return video data(file name hash code, ext, etc...)
"""
@app.route("/sld", methods=["POST"])
def server_local_download():
	ytdl.ytdl_test()
	hash = request.form["hash"]
	url = "https://youtu.be/"+hash
	time_hash = ytdl.download_video(url)
	file_names = glob(f"download/{hash}{time_hash}.*")
	file_path = f"{file_names[0]}"
	ext = "mp4" if  file_path[-1] == "4" else "webm"
	mimetype = "video"

	print(f"file name list : {file_names}")
	print(f"file path : {file_path}...{file_path[-1]}")
	print(f"ext : {ext}")

	return jsonify(
		time_hash = time_hash,
		file_names = file_names,
		file_path = file_path,
		ext = ext,
        mimetype = mimetype
	)

"""
sldao = server local download audio only
audio downloadon local
return json audio data
"""
@app.route("/sldao", methods=["POST"])
def server_local_download_audio_only():
    ytdl.ytdl_test()
    hash = request.form["hash"]
    url = "https://youtu.be/"+hash
    print("=======================")
    print("=   audio downloads   =")
    print("=======================")
    time_hash = ytdl.download_audio_only(url,hash)
    file_names = glob(f"download/*{hash}{time_hash}.*")
    file_path = f"{file_names[0]}"
    # ext = "m4a" if  file_path[-1] == "a" else "webm"
    ext = file_path.strip().split(".")[-1]
    mimetype = "audio"

    print(f"file name list : {file_names}")
    print(f"file path : {file_path}...{file_path[-1]}")
    print(f"ext : {ext}")
    
    return jsonify(
        time_hash = time_hash,
        file_names = file_names,
        file_path = file_path,
        ext = ext,
        mimetype = mimetype
    ) 

"""
sf = send file
send video file
"""
@app.route("/sf", methods=["POST"])
def send_files():
	print("send file")
	file_path = request.form["path"]
	hash = request.form["hash_code"]
	ext = request.form["ext"]
	mimetype = request.form["mimetype"]+"/"
	if(mimetype=="video/"):
		mimetype += ext
	else:
		mimetype += "*"
		ext = "mp3"

	@after_this_request
	def remove_file(response):
		try:
			print(f"삭제 파일 : {file_path}")
			if(os.path.isfile(file_path)):
				os.remove(file_path)
				print(f"{file_path} 삭제 완료")
		except:
			print("remov Error")
		return response

	print("download yes")
	return send_file(
		file_path,
		mimetype=f"{mimetype}/{ext}",
		download_name=f"{hash}.{ext}",
		as_attachment=True
	)
	
@app.route("/rm", methods=["POST"])
def rm_file():
	file_path = request.form["path"]
	print(f"rm {file_path}")
	try:
		print(f"삭제 파일 : {file_path}")
		if(os.path.isfile(file_path)):
			os.remove(file_path)
			print(f"{file_path} 삭제 완료")
	except:
		print("remov Error")
	
	return redirect("/")

def yes_or_no():
	debug_mod = argv[1]
	if(debug_mod not in set(["Yes","yes","No","no"])):
		print("yes or no...")
		exit()
	return debug_mod in set(["Yes","yes"])

def port_input():
    if(len(argv)<3 or argv[2] == ""):
        return "8080"

    port_num = argv[2]
    try:
        num = int(port_num)
    except:
        print("input num plz")
        exit()
    return port_num

app.run(debug=yes_or_no(), host="0.0.0.0", port=port_input())
