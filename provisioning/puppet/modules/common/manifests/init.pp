class common {

  exec { "apt-update":
    command => "/usr/bin/apt-get update",
    onlyif => "/bin/bash -c 'exit $(( $(( $(date +%s) - $(stat -c %Y /var/lib/apt/lists/$( ls /var/lib/apt/lists/ -tr1|tail -1 )) )) <= 604800 ))'"
  }

  package { "curl":
    ensure => latest
  }

  package { "screen":
      ensure => latest
  }

  Exec["apt-update"] -> Package <| |>

  file { "saneshell.sh":
    path    => "/etc/profile.d/saneshell.sh",
    ensure  => file,
    mode    => '0644',
    source  => "/vagrant/provisioning/puppet/modules/common/files/saneshell.sh",
    owner   => "root",
    group   => "root"
  }

  file { ".screenrc":
    path    => "/home/vagrant/.screenrc",
    ensure  => file,
    mode    => '0644',
    source  => "/vagrant/provisioning/puppet/modules/common/files/screenrc",
    owner   => "vagrant",
    group   => "vagrant"
  }

}
