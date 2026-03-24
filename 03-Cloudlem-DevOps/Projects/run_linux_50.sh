#!/bin/zsh
set +e
LAB="/Users/prom1/Desktop/Cloudlem Tasks/1/week1/linux-lab"
OUT="/Users/prom1/Desktop/Cloudlem Tasks/1/week1/linux-50-commands-output.txt"
mkdir -p "$LAB"
rm -rf "$LAB"/*
mkdir -p "$LAB/folder" "$LAB/folder_to_delete" "$LAB/folder_for_tar"
cd "$LAB" || exit 1
printf "alpha\nbeta\nGamma\ntext line\nanother Text\n" > file.txt
printf "log-start\n" > file.log
printf "inside folder\n" > folder/note.txt
printf "a\nb\nc\n" > file1
printf "x\ny\nz\n" > old
printf "tar data\n" > folder_for_tar/data.txt

run_cmd() {
  num="$1"
  cmd="$2"
  echo "========== ${num}. ${cmd} ==========" >> "$OUT"
  zsh -c "cd \"$LAB\" && $cmd" >> "$OUT" 2>&1
  echo >> "$OUT"
}

: > "$OUT"
run_cmd 1  'pwd'
run_cmd 2  'ls'
run_cmd 3  'ls -l'
run_cmd 4  'ls -a'
run_cmd 5  'cd folder && pwd'
run_cmd 6  'cd folder && cd .. && pwd'
run_cmd 7  'cd /tmp && pwd'
run_cmd 8  'mkdir newfolder && ls -d newfolder'
run_cmd 9  'rmdir folder_to_delete && echo removed_folder_to_delete'
run_cmd 10 'touch file_created.txt && ls file_created.txt'
run_cmd 11 'cp file1 file2 && ls file2'
run_cmd 12 'mv old new && ls new'
run_cmd 13 'rm file_created.txt && echo removed_file_created.txt'
run_cmd 14 'rm -r newfolder && echo removed_newfolder'
run_cmd 15 'cat file.txt'
run_cmd 16 'more file.txt | head -n 10'
run_cmd 17 'LESS=FRSX less file.txt | head -n 10'
run_cmd 18 'head file.txt'
run_cmd 19 'tail file.txt'
run_cmd 20 '(tail -f file.log & pid=$!; sleep 1; echo "new log line" >> file.log; sleep 1; kill $pid >/dev/null 2>&1)'
run_cmd 21 'whoami'
run_cmd 22 'hostname'
run_cmd 23 'date'
run_cmd 24 'uptime'
run_cmd 25 'uname -a'
run_cmd 26 'if command -v free >/dev/null 2>&1; then free -h; else echo "free not available; using vm_stat"; vm_stat | head -n 12; fi'
run_cmd 27 'df -h'
run_cmd 28 'top -l 1 | head -n 20'
run_cmd 29 'if command -v htop >/dev/null 2>&1; then htop --version; else echo "htop not installed"; top -l 1 | head -n 5; fi'
run_cmd 30 'ps aux | head -n 15'
run_cmd 31 'grep "text" file.txt'
run_cmd 32 'grep -i "text" file.txt'
run_cmd 33 'find . -name "*.txt"'
run_cmd 34 'wc -l file.txt'
run_cmd 35 'sort file.txt'
run_cmd 36 'ping -c 3 google.com'
run_cmd 37 'curl -I http://example.com'
run_cmd 38 'ifconfig || ip addr'
run_cmd 39 'if [[ "$(uname)" == "Linux" ]] && netstat -tulpn >/dev/null 2>&1; then netstat -tulpn; else echo "netstat -tulpn not supported on this OS; showing netstat summary"; netstat -an | head -n 40; fi'
run_cmd 40 'if command -v ss >/dev/null 2>&1; then ss -tulpn; else echo "ss not available; showing lsof network summary"; lsof -nP -i | head -n 30; fi'
run_cmd 41 'if command -v apt >/dev/null 2>&1; then sudo -n apt update || echo "sudo apt update needs interactive sudo"; else echo "apt not available on this OS"; fi'
run_cmd 42 'if command -v apt >/dev/null 2>&1; then sudo -n apt upgrade -y || echo "sudo apt upgrade needs interactive sudo"; else echo "apt not available on this OS"; fi'
run_cmd 43 'if command -v apt >/dev/null 2>&1; then sudo -n apt install nginx -y || echo "sudo apt install needs interactive sudo"; else echo "apt not available on this OS"; fi'
run_cmd 44 'if command -v apt >/dev/null 2>&1; then sudo -n apt remove nginx -y || echo "sudo apt remove needs interactive sudo"; else echo "apt not available on this OS"; fi'
run_cmd 45 'chmod 755 file.txt && ls -l file.txt'
run_cmd 46 'chown $(whoami):staff file.txt && ls -l file.txt'
run_cmd 47 'tar -cvf archive.tar folder_for_tar'
run_cmd 48 'mkdir -p extracted && tar -xvf archive.tar -C extracted && ls extracted'
run_cmd 49 'zip file.zip file.txt'
run_cmd 50 'unzip -o file.zip -d unzipped && ls unzipped'

echo "Saved: $OUT"
wc -l "$OUT"
