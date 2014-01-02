class lamp {

  package { "tasksel":
      ensure => latest
  }

  package { "debconf-utils":
      ensure => latest,
      before => File["debconf_selections"],
  }

  file { "debconf_selections":
    path    => "/tmp/debconf_selections",
    ensure  => file,
    mode    => '0644',
    source  => "/vagrant/provisioning/puppet/modules/lamp/files/debconf_selections",
    owner   => "root",
    group   => "root"
  }

  exec { "debconf_setup":
    command => "/usr/bin/debconf-set-selections /tmp/debconf_selections",
    creates => "/usr/sbin/apache2ctl",
    subscribe => File["debconf_selections"],
  }

  exec { "tasksel lamp":
    command => "/usr/bin/tasksel install lamp-server",
    creates => "/usr/sbin/apache2ctl",
    require => Exec["debconf_setup"],
  }

  package { "phpmyadmin":
    ensure => latest,
    require => Exec["tasksel lamp"],
  }

  file { "info.php":
    path    => "/var/www/info.php",
    ensure  => file,
    mode    => '0644',
    content => "<?php phpinfo(); ?>",
    owner   => "www-data",
    group   => "www-data",
    require => Exec["tasksel lamp"],
  }

}
