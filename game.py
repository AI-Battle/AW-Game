import json
import os
import subprocess
import threading
import time

cwd = os.getcwd()


def write_to_file(path, text):
	file = open(path, 'w')
	file.write(text)
	file.close()


def server(server_path, coremask, game_dir):
	process = subprocess.run(['taskset', hex(coremask), server_path + '/run.sh', '--config=' + game_dir + '/server.conf'], cwd=game_dir, check=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	write_to_file(game_dir + '/server.log', output)


def client(submission, coremask, game_dir):
	process = subprocess.run(['taskset', hex(coremask), submission.compiled_file_path + '/run.sh'], cwd=game_dir, check=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	write_to_file(game_dir + '/client_' + str(submission.id) + '.log', output)


def run(submissions, game_id, map_name):
	game_dir = cwd + '/games/' + str(game_id)
	try:
		os.mkdir(game_dir)

		config = {"Map": cwd + "/maps/" + map_name, "ClientsConnectionTimeout": "90000"}

		for i in range(len(submissions)):
			config["TeamName" + str(i)] = submissions[i].name

		write_to_file(game_dir + "/server.conf", json.dumps(config))

		coremask = 1

		# run server
		threading.Thread(target=server, args=(cwd + '/server', coremask, game_dir)).start()
		time.sleep(0.2)

		# run clients
		for submission in submissions:
			coremask *= 2
			threading.Thread(target=client, args=(submission, coremask, game_dir)).start()
			time.sleep(0.2)

		return 1
	except Exception as Error:
		print(Error)
		error_file = open(game_dir + '/error.log', 'w')
		error_file.write(str(Error))
		error_file.close()
		return 0


def get_result(game_id):
	try:
		a = ""
		game_dir = cwd + '/games/' + str(game_id)
		log = open(game_dir + '/graphic.log', 'r')
		for i in log.readlines():
			a = i
		q = 0
		for i in range(len(a) - 6):
			if a[i:i + 6] == 'scores':
				q = i
				break

		m = ''
		n = ''
		z = 0
		for i in range(q + 6, q + 20):
			try:
				if z == 0 or 1:
					m += a[i]
					z = 1
				if z == 2:
					n += a[i]
			except:
				if z == 1:
					z = 2
		return [m, n]
	except:
		pass
