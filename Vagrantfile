# -*- mode: ruby -*-

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu-precise12042-x64-vbox43"
  config.vm.box_url = "http://box.puphpet.com/ubuntu-precise12042-x64-vbox43.box"
  # config.vm.hostname

  config.vm.network "forwarded_port", guest: 80, host: 8888
  config.vm.network "private_network", ip: "192.168.33.100"

  # use NFS for /vagrant folder, speed on built in folder sharing is very bad
  config.vm.synced_folder ".", "/vagrant", type: "nfs"

  config.vm.provider "virtualbox" do |vbox|
    vbox.customize ["modifyvm", :id, "--memory", 1024]
    vbox.customize ["modifyvm", :id, "--cpus", 2]
    vbox.customize ["modifyvm", :id, "--cpuexecutioncap", 90]
  end

  config.vm.provision :ansible do |ansible|
    ansible.playbook = "provisioning/ansible/base.yml"
    ansible.inventory_path = "provisioning/ansible/hosts"
    ansible.verbose = "v"
  end
end
