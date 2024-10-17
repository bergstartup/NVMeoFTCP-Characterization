import http.server
import socketserver
import urllib.parse
import subprocess
import threading
import os
import signal

PORT = 8080
processes = {}

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed_path.query)
        
        if parsed_path.path == '/start':
            self.handle_start(query)
        elif parsed_path.path == '/stop':
            self.handle_stop(query)
        elif parsed_path.path == '/sched':
            self.handle_sched(query)
        elif parsed_path.path == '/poll':
            self.handle_poll(query)
        elif parsed_path.path == '/bpf':
            self.handle_bpf(query)
        elif parsed_path.path == '/sbpf':
            self.handle_sbpf(query)
        elif parsed_path.path == "/fctrl":
            self.handle_fctrl(query)
        elif parsed_path.path == "/remfctrl":
            self.handle_rfctrl(query)
        elif parsed_path.path == "/rss":
            self.handle_rss(query)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Invalid endpoint")
    
    def handle_poll(self, query):
        if 'poll' in query:
            poll = query['poll'][0]
            command = "echo {} | sudo tee -a /sys/module/nvmet_tcp/parameters/idle_poll_period_usecs".format(poll)
            subprocess.run(command, shell=True)
            print(command)

    def handle_sched(self, query):
        if 'sched' in query:
            sched = query['sched'][0]
            device = query['dev'][0]
            command = "echo {} | sudo tee -a /sys/block/{}/queue/scheduler".format(sched, device)
            subprocess.run(command, shell=True)
            print(command)

    def handle_start(self, query):
        if 'id' in query:
            id = query['id'][0]
            command = "exec sar -P ALL 1 > {}".format(id)
            print("Start : ",id, command)
            if id in processes:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Process with this ID already running\n")
                return

            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            processes[id] = process
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"Started process with ID: {id}\n".encode())
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing id or command parameter\n")

    def handle_stop(self, query):
        if 'id' in query:
            id = query['id'][0] 
            print("Stop : ",id)
            if id in processes:
                process = processes[id]
                process.send_signal(signal.SIGINT)
                process.wait()
                del processes[id]
                
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f"Stopped process with ID: {id}\n".encode())
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"No process found with this ID")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing id parameter")
    
    def handle_bpf(self, query):
        id = query['id'][0]
        script = query['script'][0]
        command = "exec ../bpf/{} > {}".format(script,id)
        print("Start : ",id, command)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        processes[id] = process

        self.send_response(200)
        self.end_headers()
        self.wfile.write(f"Started process with ID: {id}\n".encode())

    def handle_sbpf(self, query):
        id = query['id'][0]
        proc = processes[id]
        #pgid = os.getpgid(proc.pid)
        #os.killpg(pgid, signal.SIGINT)
        proc.send_signal(signal.SIGINT)
        proc.wait()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(f"Stopped process with ID: {id}\n".encode())

    def handle_rss(self, query):
        count = query['count'][0]
        command = "exec ethtool -X ens6np0 start 0 equal {}".format(count)
        subprocess.run(command, shell=True)

    def handle_fctrl(self, query):
        port = query['port'][0]
        id = query['id'][0]
        queue = query['q'][0]
        command = "exec ../setup/flow_action.sh {} {} {}".format(port, id, queue)
        subprocess.run(command, shell=True)

    def handle_rfctrl(self, query):
        total = query['total'][0]
        for i in range(int(total)):
            command = "exec ethtool -N ens6np0 delete {}".format(i)
            subprocess.run(command, shell=True)

def run_server():
    with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()

