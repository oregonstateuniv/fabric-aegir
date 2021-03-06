# Copyright (C) 2013 Oregon State University
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
#
# To contact us, go to http://oregonstate.edu/cws/contact and fill out the contact form.
#
# Alternatively mail us at:
#
# Oregon State University
# Central Web Services
# 121 The Valley Library
# Corvallis, OR 97331

from fabric.api import *
from fabric.colors import *

# Save the Drush alias for a new server
# @params
#	host 	-> hostname
#	type 	-> mysql, apache, pr pack
#	db   	-> connect string for database server
#	master	-> For pack master server
#	slave	-> For pack list of slaves
#
# drush provision-save @server_$hostname
# 	--remote_host                             server: host name; default localhost
#	--script_user                             server: OS user name; default current user
#	--aegir_root                              server: Aegir root; default /var/aegir
#	--master_url                              server: Hostmaster URL
#	--db_service_type                         server: mysql, or null; default null
#	--master_db                               server with db: Master database connection info, {type}://{user}:{password}@{host}
#	--dns_service_type                        server: bind, dnsmasq, or null; default null
#	--example_service_type                    server: basic, or null; default null
#	--http_service_type                       server: nginx, cluster, apache, pack, or null; default null
#	--web_group                               server with http: OS group for permissions; working default will be attempted
#	--cluster_web_servers                     server with cluster: comma-separated list of web servers.
#	--slave_web_servers                       server with pack: comma-separated list of slave web servers.
#	--master_web_servers                      server with pack: comma-separated list of master web servers.




def server_save_alias(hostname, type, db_str, master, slave):
	print(green("Creating or updating the Drush alias for %s." % hostname))

	server_alias 		= '@server_' + hostname
	server_fqn			= hostname + '.cws.oregonstate.edu'
	master_url			= 'http://aegir-vd10.cws.oregonstate.edu'
	master_alias		= '@hostmaster'
	db_service_type   	= ''
	http_service_type 	= ''
	web_group 		  	= ''

	if type == 'mysql':
		db_service_type   = 'mysql'

	elif type == 'apache':
		http_service_type = 'apache'
		web_group 		  = 'apache'

	elif type == 'pack':
		http_service_type = 'pack'
		web_group 		  = 'apache'

	run("drush provision-save %s \
		--context_type=server \
		--remote_host=%s \
		--master_url=%s \
		--db_service_type=%s \
		--master_db=%s \
		--http_service_type=%s \
		--slave_web_servers=%s \
		--master_web_servers=%s" \
		% (server_alias, server_fqn, master_url, db_service_type, db_str, http_service_type, slave, master ))

	run("drush @hostmaster hosting-import %s" % server_alias)
