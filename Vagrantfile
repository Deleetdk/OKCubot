# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  config.vm.hostname = "okcubot"

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "precise64"

  # The url from where the 'config.vm.box' box will be fetched if it
  # doesn't already exist on the user's system.
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network :forwarded_port, guest: 80, host: 8080

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network :private_network, ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network :public_network

  # If true, then any SSH connections made will enable agent forwarding.
  # Default value: false
  config.ssh.forward_agent = true

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider :virtualbox do |vb|
  #   # Don't boot with headless mode
  #   vb.gui = true
  #
  #   # Use VBoxManage to customize the VM. For example to change memory:
    vb.customize ["modifyvm", :id, "--memory", "512"]
  end
  #
  # View the documentation for the provider you're using for more
  # information on available options.

  config.vm.provision :shell do |shell|
    if File.exists?(Dir.home + '/.gitconfig')
      shell.args = "'#{File.read(Dir.home + '/.gitconfig').strip.gsub!(/\n/, '\n')}'"
    end
    shell.inline = setup_project(config.vm.hostname)
  end
end

# shell script to set up project
def setup_project(project)
  return <<-EOS
    export PROJECT=#{project}

    export PYTHON_VERSION=2.7
    export SETUPTOOLS_VERSION=1.1.6
    export VIRTUALENVWRAPPER_VERSION=4.1.1

    export VAGRANT_USER=vagrant
    export VAGRANT_HOME=/home/$VAGRANT_USER

    if [ -n "$1" ]; then
      echo -e $1 > $VAGRANT_HOME/.gitconfig
      chown $VAGRANT_USER.$VAGRANT_USER $VAGRANT_HOME/.gitconfig
    fi

    apt-get update
    apt-get install -y build-essential curl git python-dev libxml2-dev \
      libxslt1-dev python-software-properties nodejs npm \
      libffi-dev libssl-dev

    ln -sf /usr/bin/nodejs /usr/bin/node

    # For building presentation slides
    npm install -g cleaver

    if [ ! -e /usr/local/bin/virtualenv-$PYTHON_VERSION ]; then
      cd $VAGRANT_HOME
      curl -ksLo virtualenv.tar.gz https://github.com/pypa/virtualenv/tarball/develop
      tar xzf virtualenv.tar.gz
      cd pypa-virtualenv*
      python$PYTHON_VERSION setup.py install
      cd $VAGRANT_HOME
      rm -rf pypa-virtualenv* virtualenv.tar.gz
    fi

    if [ ! -e /usr/local/lib/python$PYTHON_VERSION/dist-packages/setuptools-$SETUPTOOLS_VERSION-py$PYTHON_VERSION.egg ]; then
      cd $VAGRANT_HOME
      curl -sO https://pypi.python.org/packages/source/s/setuptools/setuptools-$SETUPTOOLS_VERSION.tar.gz
      tar xzf setuptools-$SETUPTOOLS_VERSION.tar.gz
      cd setuptools-$SETUPTOOLS_VERSION
      python$PYTHON_VERSION setup.py install
      cd $VAGRANT_HOME
      rm -rf setuptools-$SETUPTOOLS_VERSION*
    fi

    if [ ! -e /usr/local/bin/pip$PYTHON_VERSION ]; then
      cd $VAGRANT_HOME
      curl -ksLo pip.tar.gz https://github.com/pypa/pip/tarball/develop
      tar xzf pip.tar.gz
      cd pypa-pip*
      python$PYTHON_VERSION setup.py install
      cd $VAGRANT_HOME
      rm -rf pypa-pip* pip.tar.gz
    fi

    if [ ! -e /usr/local/lib/python$PYTHON_VERSION/dist-packages/virtualenvwrapper-$VIRTUALENVWRAPPER_VERSION-py$PYTHON_VERSION.egg-info ]; then
      cd $VAGRANT_HOME
      curl -ksLO https://pypi.python.org/packages/source/v/virtualenvwrapper/virtualenvwrapper-$VIRTUALENVWRAPPER_VERSION.tar.gz
      tar xzf virtualenvwrapper-$VIRTUALENVWRAPPER_VERSION.tar.gz
      cd virtualenvwrapper-$VIRTUALENVWRAPPER_VERSION
      python$PYTHON_VERSION setup.py install
      cd $VAGRANT_HOME
      rm -rf virtualenvwrapper-$VIRTUALENVWRAPPER_VERSION*
    fi

    if ! grep -q WORKON_HOME $VAGRANT_HOME/.bashrc; then
      echo >> $VAGRANT_HOME/.bashrc
      echo 'export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python'$PYTHON_VERSION >> $VAGRANT_HOME/.bashrc
      echo 'export WORKON_HOME=$HOME/.virtualenvs' >> $VAGRANT_HOME/.bashrc
      echo 'export PROJECT_HOME=/vagrant' >> $VAGRANT_HOME/.bashrc
      echo 'source /usr/local/bin/virtualenvwrapper.sh' >> $VAGRANT_HOME/.bashrc
    fi

    if ! grep -q 'alias co=' $VAGRANT_HOME/.bashrc; then
      echo >> $VAGRANT_HOME/.bashrc
      echo 'alias co="cd /vagrant"' >> $VAGRANT_HOME/.bashrc
    fi

    if ! grep -q 'EDITOR=' $VAGRANT_HOME/.bashrc; then
      echo >> $VAGRANT_HOME/.bashrc
      echo 'export EDITOR=vim' >> $VAGRANT_HOME/.bashrc
    fi

    if ! grep -q "workon $PROJECT" $VAGRANT_HOME/.profile; then
      echo >> $VAGRANT_HOME/.profile
      echo "workon $PROJECT" >> $VAGRANT_HOME/.profile
    fi

    if [ ! -e $VAGRANT_HOME/.virtualenvs/$PROJECT ]; then
      mkdir -p $VAGRANT_HOME/.virtualenvs
      echo "virtualenv --system-site-packages $VAGRANT_HOME/.virtualenvs/$PROJECT"
      virtualenv -q --system-site-packages $VAGRANT_HOME/.virtualenvs/$PROJECT

      echo "#!/bin/bash" > $VAGRANT_HOME/.virtualenvs/$PROJECT/bin/postactivate
      echo "export PYTHONPATH=/vagrant" >> $VAGRANT_HOME/.virtualenvs/$PROJECT/bin/postactivate
      chmod 775 $VAGRANT_HOME/.virtualenvs/$PROJECT/bin/postactivate

      echo "#!/bin/bash" > $VAGRANT_HOME/.virtualenvs/$PROJECT/bin/postdeactivate
      echo "unset PYTHONPATH" >> $VAGRANT_HOME/.virtualenvs/$PROJECT/bin/postdeactivate
      chmod 775 $VAGRANT_HOME/.virtualenvs/$PROJECT/bin/postdeactivate

      chown -R $VAGRANT_USER.$VAGRANT_USER $VAGRANT_HOME/.virtualenvs
    fi

    # Install requirements
    pip install -r /vagrant/requirements.txt

    # Cleanup veewee post install scripts
    if [[ -e $VAGRANT_HOME/vagrant.sh || -e $VAGRANT_HOME/postinstall.sh ]]; then
      rm $VAGRANT_HOME/{apt,build_time,chef,cleanup,postinstall,ruby,sudo,vagrant,vbox}.sh
    fi
  EOS
end