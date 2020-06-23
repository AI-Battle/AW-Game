import os
import shutil
import subprocess
import zipfile

cwd = os.getcwd()


def unzip(submission_dir):
	with zipfile.ZipFile(submission_dir + "/client.zip", 'r') as zip_ref:
		zip_ref.extractall(submission_dir + "/source")


def java(submission_id):
	submission_dir = cwd + "/submissions/" + str(submission_id)
	try:
		try:
			shutil.rmtree(submission_dir + "/source")
		except:
			pass
		# unzipping submitted client
		unzip(submission_dir)

		source_dir = submission_dir + "/source/" + os.listdir(submission_dir + "/source")[0]
		build_dir = submission_dir + "/build"
		client_path = submission_dir + "/client.jar"

		# compile client
		java_files = []
		jar_files = []
		for (dirpath, _, filenames) in os.walk(source_dir):
			p = [os.path.join(dirpath, f) for f in filenames if f[-5:] == '.java']
			java_files.extend(p)
			p = [os.path.join(dirpath, f) for f in filenames if f[-4:] == '.jar']
			jar_files.extend(p)
		try:
			os.remove(client_path)
		except:
			pass
		try:
			shutil.rmtree(build_dir)
		except:
			pass
		os.mkdir(build_dir)
		subprocess.run(['javac', '-d', build_dir, '-classpath', ':'.join(jar_files) + ':'] + java_files, check=True, stdout=subprocess.PIPE, universal_newlines=True)
		for jar_file in jar_files:
			subprocess.run(['unzip', jar_file, '-x', 'META-INF/MANIFEST.MF', '-d', build_dir], check=True, stdout=subprocess.PIPE, universal_newlines=True)
		subprocess.run(['jar', '-cvfe', client_path, 'client.Main', './'], check=True, stdout=subprocess.PIPE, universal_newlines=True, cwd=build_dir)
		shutil.rmtree(submission_dir + "/source")
		shutil.rmtree(build_dir)

		# create client runner file
		file = open(submission_dir + "/run.sh", 'w')
		file.write("timeout -m " + str(1024 ** 3) + " -t 150 java -jar '" + client_path + "'")
		file.close()
		os.system("chmod +x '" + submission_dir + "/run.sh'")

		return 1
	except Exception as Error:
		print(str(Error))
		file = open(submission_dir + "/error.log", 'w')
		file.write(str(Error))
		file.close()

		return 0


def cpp(submission_id):
	submission_dir = cwd + "/submissions/" + str(submission_id)
	try:
		try:
			shutil.rmtree(submission_dir + "/source")
		except:
			pass
		# unzipping submitted client
		unzip(submission_dir)

		source_dir = submission_dir + "/source/" + os.listdir(submission_dir + "/source")[0]
		build_dir = os.path.join(source_dir, 'build')
		client_path = submission_dir + "/client"

		# compile client
		try:
			os.remove(client_path)
		except:
			pass
		try:
			shutil.rmtree(build_dir)
		except:
			pass
		os.mkdir(build_dir)
		subprocess.run(['cmake', '-S', source_dir, '-B', build_dir], check=True, stdout=subprocess.PIPE, universal_newlines=True)
		subprocess.run(['make', '-C', build_dir], check=True, stdout=subprocess.PIPE, universal_newlines=True)
		shutil.move(build_dir + '/client/client', client_path)
		shutil.rmtree(submission_dir + "/source")

		# create client runner file
		file = open(submission_dir + "/run.sh", 'w')
		file.write("timeout -m " + str(1024 ** 3) + " -t 150 '" + client_path + "'")
		file.close()
		os.system("chmod +x '" + submission_dir + "/run.sh'")

		return 1
	except Exception as Error:
		print(str(Error))
		file = open(submission_dir + "/error.log", 'w')
		file.write(str(Error))
		file.close()

		return 0


def python(submission_id):
	submission_dir = cwd + "/submissions/" + str(submission_id)
	try:
		try:
			shutil.rmtree(submission_dir + "/source")
		except:
			pass
		# unzipping submitted client
		unzip(submission_dir)

		source_dir = submission_dir + "/source/" + os.listdir(submission_dir + "/source")[0]
		client_path = submission_dir + "/client"

		# move source to specific folder
		try:
			shutil.rmtree(client_path)
		except:
			pass
		shutil.move(source_dir, client_path)
		shutil.rmtree(submission_dir + "/source")

		# create client runner file
		file = open(submission_dir + "/run.sh", 'w')
		file.write("timeout -m " + str(1024 ** 3) + " -t 150 python3 '" + client_path + "/Controller.py'")
		file.close()
		os.system("chmod +x '" + submission_dir + "/run.sh'")

		return 1
	except Exception as Error:
		print(str(Error))
		file = open(submission_dir + "/error.log", 'w')
		file.write(str(Error))
		file.close()

		return 0
