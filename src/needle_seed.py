from subprocess import Popen, PIPE

def search(inputs):
    p = Popen(['./qr'], stdin=PIPE, stdout=PIPE, cwd="./lib/QR-Database")
    stdout, stderr = p.communicate(inputs.encode('utf-8'))
    p.terminate()
    return [x.split() for x in stdout.decode('utf-8').split("\n") if x]

if __name__ == '__main__':
    print(run("10 1 9 3 7 8 4 16 1 14 13"))
