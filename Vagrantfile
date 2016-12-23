# -*- mode: ruby -*-
# vi: set ft=ruby :
#
# Vagrantfile for developement of the ZenPacks.community.Fortinet zenpack
#

BASEDIR = File.expand_path(File.dirname(__FILE__))

# automatic plugin installation
# the guest additions does not work at first boot but at 2nd. Ok so
require File.dirname(__FILE__) + "/dependency_manager"
check_plugins ["vagrant-vbguest", "vagrant-timezone"]

Vagrant.configure("2") do |config|
    if Vagrant.has_plugin?("vagrant-timezone")
        config.timezone.value = "Europe/Zurich"
    end

    config.vm.provider "virtualbox" do |virtualbox|
      virtualbox.cpus = 2
      virtualbox.memory = 8192
      virtualbox.name = 'dev_zenpack_fortinet'
      virtualbox.customize ["modifyvm", :id, "--ioapic", "on"]
      virtualbox.customize ["modifyvm", :id, "--vram", "16"]
    end

    config.vm.define :zenoss do |box|
      box.vm.box = 'puppetlabs/centos-6.6-64-puppet'
      box.vm.hostname = 'zenoss.msp'

      box.vm.provision "shell", inline: <<-SCRIPT

        # explicit BE proxies to avoid WCCP
        #export https_proxy=http://10.249.255.5:8080
        # export http_proxy=http://10.249.255.5:8080
        echo "using this proxy setup :"
        env | grep -i proxy

        chkconfig iptables off
        service iptables stop

        # fix iTerm for OSX
        grep LC_CTYPE /etc/sysconfig/i18n > /dev/null || echo 'LC_CTYPE="en_US.UTF-8"' >> /etc/sysconfig/i18n

        echo "zenoss user and group"
        groupadd -g 1001 zenoss
        useradd -u 1337 -g zenoss -m -d /home/zenoss -s /bin/bash zenoss

        # old broken code
        # echo "get zenoss auto-deploy"
        # test -f auto.tar.gz || wget -q https://github.com/zenoss/core-autodeploy/tarball/4.2.5 -O auto.tar.gz
        # tar xvf auto.tar.gz
        # ls zenoss-core-autodeploy-* &> /dev/null || exit
        # cd zenoss-core-autodeploy-*
        # cp core-autodeploy.sh core-autodeploy.sh_save
        # sed -i '11,30d' core-autodeploy.sh

        # new code from https://gate.msp.ccsn.ch/confluence/display/MSP/Basic+Installation
        echo "get zenoss auto-deploy"
        test -f auto.tar.gz || wget -q https://github.com/zenoss/core-autodeploy/tarball/4.2.5 -O auto.tar.gz
        tar xvf auto.tar.gz
        ls zenoss-core-autodeploy-* &> /dev/null || exit
        cd zenoss-core-autodeploy-*
        cp core-autodeploy.sh core-autodeploy.sh_save
        sed -i '11,30d' core-autodeploy.sh
        # RPMforge dead. Use dev.zenoss repo
        sed -i '216,222d' core-autodeploy.sh
        sed -i '216 i rpm -ivh http://deps.zenoss.com/yum/zenossdeps-4.2.x-1.el6.noarch.rpm' core-autodeploy.sh
        sed -i '217 i yum -y install rrdtool' core-autodeploy.sh

        yum -y remove mysql-libs
        yum -y install epel-release
        # cp /etc/yum.repos.d/epel.repo /tmp/epel.repo_save
        sed -i -e '/mirrorlist/d' -e 's/#baseurl/baseurl/' /etc/yum.repos.d/epel.repo

        AUTO_INSTALL_LOG=/tmp/zenoss_auto_deploy.log
        echo "--------------------------------------------------------------------------------------"
        echo "deploy zenoss package, be patient. Logfile: $AUTO_INSTALL_LOG"
        echo "--------------------------------------------------------------------------------------"
        ./core-autodeploy.sh > $AUTO_INSTALL_LOG 2>&1

        # for PyYAML in zenoss python
        yum -y install libyaml
        yum -y install libyaml-devel

        # SNMP command-line tools
        yum -y install net-snmp-utils

        # development tools
        yum -y install git
        yum -y install unzip

        # set environment and password of zenoss user
        echo 'if [ -f ~/.bashrc ]; then' > /home/zenoss/.bash_profile
        echo '    . ~/.bashrc' >> /home/zenoss/.bash_profile
        echo 'fi' >> /home/zenoss/.bash_profile

        mv -f /home/zenoss/.bashrc /tmp/
        echo 'if [ -f /etc/bashrc ]; then' > /home/zenoss/.bashrc
        echo '    . /etc/bashrc' >> /home/zenoss/.bashrc
        echo 'fi' >> /home/zenoss/.bashrc
        echo '' >> /home/zenoss/.bashrc
        cat /tmp/.bashrc >> /home/zenoss/.bashrc

        chown -R zenoss:zenoss /home/zenoss
        echo 'zenoss' | passwd --stdin zenoss

        # slow, think before enabling, consider running it manually later
        #yum update -y

        echo "INFO: zenoss auto-deploy logfile is: $AUTO_INSTALL_LOG"
        echo "INFO: consider rebooting to apply the new packages updates"

      SCRIPT

      box.vm.network :forwarded_port, host: 8888, guest: 8080
      config.vm.synced_folder ".",
        "/tmp/#{File.basename(File.expand_path(File.dirname(__FILE__)))}",
        owner: 1337,
        group: 501
    end
end
