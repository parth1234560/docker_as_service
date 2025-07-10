
import streamlit as st
import os
with st.container():
    st.subheader("🐳 Remote Docker Menu via SSH")
    st.markdown("Enter your SSH details to manage Docker remotely:")

    import paramiko

    host = st.text_input("🌍 SSH Host (e.g., 192.168.1.10)")
    username1 = st.text_input("👤 SSH Username")
    password = st.text_input("🔑 SSH Password", type="password")

    # SSH command executor
    def run_remote_command(cmd):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host, username=username1, password=password, timeout=5)
            stdin, stdout, stderr = ssh.exec_command(cmd)
            out = stdout.read().decode()
            err = stderr.read().decode()
            ssh.close()
            return out if out else err
        except Exception as e:
            return f"❌ SSH ERROR: {e}"

    if host and username1 and password:
        st.success("✅ SSH credentials validated.")

        menu = st.selectbox("📋 Choose Docker Operation", [
            "Start a Container",
            "Stop a Container",
            "Remove a Container",
            "List Docker Images",
            "List All Containers",
            "Pull a Docker Image",
            "Run a Docker Image",
            "Exit"
        ])

        if menu == "Start a Container":
            st.code(run_remote_command("docker ps -a"))
            container = st.text_input("🧱 Enter container name to start:")
            if st.button("🚀 Start Container"):
                st.code(run_remote_command(f"docker start {container}"))

        elif menu == "Stop a Container":
            st.code(run_remote_command("docker ps -a"))
            container = st.text_input("🛑 Enter container name to stop:")
            if st.button("✋ Stop Container"):
                st.code(run_remote_command(f"docker stop {container}"))

        elif menu == "Remove a Container":
            st.code(run_remote_command("docker ps -a"))
            container = st.text_input("🗑️ Enter container name to remove:")
            if st.button("❌ Remove Container"):
                st.code(run_remote_command(f"docker rm {container}"))

        elif menu == "List Docker Images":
            if st.button("📦 Show Docker Images"):
                st.code(run_remote_command("docker images"))

        elif menu == "List All Containers":
            if st.button("📋 Show All Containers"):
                st.code(run_remote_command("docker ps -a"))

        elif menu == "Pull a Docker Image":
            image = st.text_input("⬇️ Enter Docker image to pull (e.g., `ubuntu:latest`):")
            if st.button("📥 Pull Image"):
                st.code(run_remote_command(f"docker pull {image}"))

        elif menu == "Run a Docker Image":
            image = st.text_input("🔧 Enter image name (e.g., `nginx`):")
            name = st.text_input("📛 Enter name for new container:")
            if st.button("🏃 Run Docker Image"):
                st.code(run_remote_command(f"docker run -dit --name {name} {image}"))

        elif menu == "Exit":
            st.info("👋 Exiting Docker Menu.")
    else:
        st.info("⏳ Waiting for valid SSH credentials to show menu.")
with st.container():
    import paramiko

    # ---------------- Page Config ----------------
    st.subheader("🐧 Top 50 RHEL Linux Commands via SSH")

    # ---------------- SSH Form ----------------
    st.subheader("🔐 Enter SSH Credentials")
    host = st.text_input("📡 SSH Host (e.g., 192.168.1.10)")
    username = st.text_input("👤 SSH Username",key="ssh_key")
    password = st.text_input("🔑 SSH Password", type="password",key="ssh_pass")

    # ---------------- Command Selection ----------------
    st.subheader("📜 Choose a Command to Run")

    linux_commands = {
        # --- System Info & Basics ---
        "pwd": "📍 Current Directory",
        "whoami": "🙋 Current User",
        "hostname": "🖥️ Hostname",
        "uname -a": "🧠 System Info",
        "uptime": "⏲️ Uptime",
        "date": "📅 Date & Time",
        "cal": "📆 Calendar",
        "top -n 1": "📊 Running Processes",
        "free -m": "💾 RAM Usage (MB)",
        "htop": "📈 Interactive Process Viewer (if installed)",

        # --- File & Directory ---
        "ls": "📁 List Files",
        "ls -l": "📁 Detailed List",
        "ls -a": "👀 List All (with hidden)",
        "cd ~ && ls": "🏠 Home Dir Content",
        "mkdir test_folder": "📂 Create Dir 'test_folder'",
        "rm -rf test_folder": "❌ Remove 'test_folder'",
        "touch newfile.txt": "📄 Create File",
        "rm newfile.txt": "🗑️ Delete File",
        "cp /etc/hosts copied_hosts": "📋 Copy File",
        "mv copied_hosts moved_hosts": "🔀 Rename File",

        # --- File Viewing ---
        "cat /etc/os-release": "📦 OS Info File",
        "head -5 /etc/passwd": "📄 First 5 lines of passwd",
        "tail -5 /etc/passwd": "📄 Last 5 lines of passwd",
        "echo Hello Linux!": "📢 Print Text",
        "wc -l /etc/passwd": "🔢 Line Count",
        "sort /etc/passwd": "🔃 Sort File",

        # --- Network ---
        "ping -c 3 google.com": "🌐 Ping Google",
        "ip a": "🌍 IP Info",
        "ifconfig": "📡 Interface Config (older)",
        "netstat -tuln": "🔌 Listening Ports",
        "ss -tuln": "🧠 Sockets",
        "curl ifconfig.me": "🌐 External IP",
        "wget http://example.com": "📥 Download File",
        "ssh localhost": "🔐 SSH Self",
        "scp /etc/hosts localhost:/tmp": "📦 Copy File via SCP",

        # --- Search & Permissions ---
        "find / -name passwd": "🔍 Find File",
        "locate passwd": "🔎 Locate File",
        "grep 'root' /etc/passwd": "🔍 Search 'root'",
        "chmod 755 test.sh": "🔒 Change Permissions",
        "chown root:root /tmp": "👑 Change Ownership",

        # --- Disk, Users, Package ---
        "df -h": "💽 Disk Usage",
        "du -sh *": "📦 Dir Size Summary",
        "lsblk": "🧱 Block Devices",
        "useradd testuser": "👤 Add User",
        "passwd testuser": "🔑 Set Password for User",
        "yum install nano -y": "📦 Install Nano"
    }

    # ---------------- Command Selection Dropdown ----------------
    selected_command = st.selectbox("💡 Select Command", options=list(linux_commands.keys()),
                                    format_func=lambda x: f"{x} — {linux_commands[x]}")

    # ---------------- Remote Execution Function ----------------
    def run_ssh_command(cmd, host, username, password):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host, username=username, password=password, timeout=5)
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            ssh.close()
            return output if output else error
        except Exception as e:
            return f"❌ SSH Error: {e}"

    # ---------------- Run on Submit ----------------
    if st.button("🚀 Run Command on RHEL"):
        if host and username and password:
            with st.spinner("Connecting via SSH and running command..."):
                result = run_ssh_command(selected_command, host, username, password)
            st.success("✅ Command Executed Successfully")
            st.markdown(f"### 📋 Output of `{selected_command}`")
            st.code(result)
        else:
            st.warning("Please fill all SSH details to connect.")