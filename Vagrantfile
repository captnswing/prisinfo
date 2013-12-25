# -*- mode: ruby -*-

Vagrant.configure("2") do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"
  # config.vm.hostname

  config.vm.network "forwarded_port", guest: 80, host: 8888
  config.vm.network "private_network", ip: "192.168.33.100"

  # use NFS for /vagrant folder, speed on built in folder sharing is very bad
  config.vm.synced_folder ".", "/vagrant", type: "nfs"

  config.vm.provider "virtualbox" do |v|
    v.customize ["modifyvm", :id, "--memory", 1024]
    v.customize ["modifyvm", :id, "--cpus", 2]
    v.customize ["modifyvm", :id, "--cpuexecutioncap", 90]
  end

  config.vm.provision :ansible do |ansible|
    ansible.playbook = "provisioning/ansible/base.yml"
    ansible.inventory_path = "provisioning/ansible/hosts"
    ansible.verbose = "v"
  end
end
