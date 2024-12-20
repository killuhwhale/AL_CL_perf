# echo "password" | sudo -S myscript.sh
# Install Java
Red="\033[31m"
Black="\033[30m"
Green="\033[32m"
Yellow="\033[33m"
Blue="\033[34m"
Purple="\033[35m"
Cyan="\033[36m"
White="\033[37m"
RESET="\033[0m"

echo "Chromebook users: press enter to submit sudo password"
sudo apt -y install default-jre

sudo apt -y install git
sudo apt -y install libnss3-dev libgdk-pixbuf2.0-dev libgtk-3-dev libxss-dev

# Setup Gcloud
sudo apt-get -y install apt-transport-https ca-certificates gnupg
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
sudo apt-get -y update && sudo apt-get -y install google-cloud-cli



# Setup Node environment

num_files=$(ls -1a $NVM_DIR | wc -l)
key_len=${#NVM_DIR}
npm=$(which npm)
npm_len=${#npm}
echo -e "\n\n $Green Checking NODE ENV: ($num_files) - ($key_len) - ($npm_len) $RESET \n\n"



if [ $num_files -gt 0 -a $key_len -gt 0 -a npm_len -gt 0 ]; then
  # If nvm is installed, print "Installed"
  echo -e "\n\n $Blue Node Installed $RESET \n\n"
else
    # If nvm is not installed, print "Not installed"
    echo -e "\n\n $Red Node Not Installed $RESET \n\n"
    echo -e "\n\n $Yellow Installing node... $RESET \n\n"
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash

    echo -e "\n\n $Blue Installed NVM $RESET \n\n"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm

    echo "If nvm or npm command not seen, run "
    echo -e "\n\n $Cyan If nvm or npm command not seen, Run: \n\t $Red exec bash $RESET \n $Cyan and rerun script! $RESET \n\n"

    source ~/.bashrc
    echo -e "\n\n $Blue Installing Node 18.7.0 $RESET \n\n"
    nvm install 18.7.0
    nvm use node
    echo -e "\n\n $Yellow Installing npm appium... $RESET \n\n"
    npm install -g appium
fi




bash append_to_bashrc.sh "export ANDROID_HOME=/home/\$USER/Android/Sdk" "/home/$USER/.bashrc"
bash append_to_bashrc.sh "export PATH=\$PATH:\$ANDROID_HOME/platform-tools:\$ANDROID_HOME/tools:\$ANDROID_HOME/build-tools;" "/home/$USER/.bashrc"
bash append_to_bashrc.sh "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64" "/home/$USER/.bashrc"
bash append_to_bashrc.sh "export PATH=\$PATH:\$JAVA_HOME" "/home/$USER/.bashrc"




if [ ! -e "/home/$USER/appium" ]; then
    echo -e "\n\n $Green Cloning repo & setting up env... $RESET \n\n"
    sudo apt-get -y install python3-venv
    git clone https://github.com/killuhwhale/appium.git
    cd appium
    python3 -m venv .
    source bin/activate
    cd src
    pip install -r requirements.txt
else
    echo -e "\n\n $Yellow Source env already setup... $RESET \n\n"
    cd appium/src
fi
echo -e "\n\n $Yellow Finished! When installing NVM and NPM for the first time,"
echo -e "\t we need to reset the env to finish the install "

echo -e "\n\n $Yellow Run the following and then rerun this script. \n\t $RESET $Red exec bash $RESET \n\n"

echo -e "\n\n $Cyan Also don't forget to activate venv:: \n\t $RESET $Red source appium/bin/activate $RESET \n\n"

echo -e "\n\n $Cyan To run: cd appium/src \n\t $RESET $Red python3 main.py 192.168.0.123:5555 192.168.0.235:5555 $RESET \n\n"

echo -e "\n\n $Cyan Don't forget to login to Gcloud CLI \n\t $RESET $Red gcloud auth login $RESET \n\n"