# 건강한 얼굴 건강한 정신

안면 인식을 통해 안면 장애를 판단하여 뇌졸중 증상을 판단하는 웹 프로젝트입니다.

<!--
# Setting Nginx and uwsgi

Need to setting this texts to launch server

## save to /FULL/PATH/YOUR/PROJECT
### filename contest_uwsgi.ini file

    [uwsgi]
    # Django-related settings
    # the base directory (full path)
    chdir           = /full/path/your/project/
    # Django's wsgi file
    module          = setting.wsgi:application
    # the virtualenv (full path)
    home            = /full/path/virtual_env

    # process-related settings
    # master
    master          = true
    # maximum number of worker processes
    processes       = 2
    # the socket (use the full path to be safe
    socket          = /full/path/your/socket
    # ... with appropriate permissions - may be needed
    chmod-socket    = 666
    # clear environment on exit
    vacuum          = true

## save to /ETC/NGINX/
### filename nginx.conf

    user www-data;
    worker_processes auto;
    pid /run/nginx.pid;
    include /etc/nginx/modules-enabled/*.conf;
    events {
            worker_connections 768;
            # multi_accept on;
    }

    http {
            upstream django {
            server unix:/full/path/your/socket; # for a file socket
            #server 127.0.0.1:8001; # for a web port socket (we'll use this first)
            }
            fastcgi_buffers 8 16k;
            fastcgi_buffer_size 32k;
            fastcgi_connect_timeout 300;
            fastcgi_send_timeout 300;
            fastcgi_read_timeout 300;

            ##
            # Basic Settings
            ##

            sendfile on;
            tcp_nopush on;
            types_hash_max_size 2048;
            # server_tokens off;

            # server_names_hash_bucket_size 64;
            # server_name_in_redirect off;

            include /etc/nginx/mime.types;
            default_type application/octet-stream;

            ##
            # SSL Settings
            ##

            ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3; # Dropping SSLv3, ref: POODLE
            ssl_prefer_server_ciphers on;

            ##
            # Logging Settings
            ##

            access_log /var/log/nginx/access.log;
            error_log /var/log/nginx/error.log;

            ##
            # Gzip Settings
            ##

            gzip on;

            # gzip_vary on;
            # gzip_proxied any;
            # gzip_comp_level 6;
            # gzip_buffers 16 8k;
            # gzip_http_version 1.1;
            # gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

            ##
            # Virtual Host Configs
            ##

            include /etc/nginx/conf.d/*.conf;
            include /etc/nginx/sites-enabled/*;
    }

## save to /etc/nginx/
### filename uwsgi_params

    uwsgi_param  QUERY_STRING       $query_string;
    uwsgi_param  REQUEST_METHOD     $request_method;
    uwsgi_param  CONTENT_TYPE       $content_type;
    uwsgi_param  CONTENT_LENGTH     $content_length;

    uwsgi_param  REQUEST_URI        $request_uri;
    uwsgi_param  PATH_INFO          $document_uri;
    uwsgi_param  DOCUMENT_ROOT      $document_root;
    uwsgi_param  SERVER_PROTOCOL    $server_protocol;
    uwsgi_param  REQUEST_SCHEME     $scheme;
    uwsgi_param  HTTPS              $https if_not_empty;

    uwsgi_param  REMOTE_ADDR        $remote_addr;
    uwsgi_param  REMOTE_PORT        $remote_port;
    uwsgi_param  SERVER_PORT        $server_port;
    uwsgi_param  SERVER_NAME        $server_name;

## save to /etc/nginx/sites-available/
### filename default

    ##
    # You should look at the following URL's in order to grasp a solid understanding
    # of Nginx configuration files in order to fully unleash the power of Nginx.
    # https://www.nginx.com/resources/wiki/start/
    # https://www.nginx.com/resources/wiki/start/topics/tutorials/config_pitfalls/
    # https://wiki.debian.org/Nginx/DirectoryStructure
    #
    # In most cases, administrators will remove this file from sites-enabled/ and
    # leave it as reference inside of sites-available where it will continue to be
    # updated by the nginx packaging team.
    #
    # This file will automatically load configuration files provided by other
    # applications, such as Drupal or Wordpress. These applications will be made
    # available underneath a path with that package name, such as /drupal8.
    #
    # Please see /usr/share/doc/nginx-doc/examples/ for more detailed examples.
    ##

    # Default server configuration
    #
    server {
            listen 80 default_server;
            listen [::]:80 default_server;

    # SSL configuration
    #
    # listen 443 ssl default_server;
    # listen [::]:443 ssl default_server;
    #
    # Note: You should disable gzip for SSL traffic.
    # See: https://bugs.debian.org/773332
    #
    # Read up on ssl_ciphers to ensure a secure configuration.
    # See: https://bugs.debian.org/765782
    #
    # Self signed certs generated by the ssl-cert package
    # Don't use them in a production server!
    #
    # include snippets/snakeoil.conf;

            root /var/www/html;

    #Add index.php to the list if you are using PHP
            index index.html index.htm index.nginx-debian.html;

            server_name _;

    #location / {
    # First attempt to serve request as file, then
    # as directory, then fall back to displaying a 404.
    #try_files $uri $uri/ =404;
    #
    #}
            location / {
    # Finally, send all non-media requests to the Django server.
                    include     /path/where/your/uwsgi_params; # the uwsgi_params file you installed
                            uwsgi_pass  django;
            }


            location /media  {
                    alias /full/path/where/your/project/media;  # your Django project's media files - amend as required
            }

            location /static {
                    alias /full/path/where/your/project/static; # your Django project's static files - amend as required
            }

    # pass PHP scripts to FastCGI server
    #
    #location ~ \.php$ {
    #       include snippets/fastcgi-php.conf;
    #
    #       # With php-fpm (or other unix sockets):
    #       fastcgi_pass unix:/run/php/php7.4-fpm.sock;
    #       # With php-cgi (or other tcp sockets):
    #       fastcgi_pass 127.0.0.1:9000;
    #}

    # deny access to .htaccess files, if Apache's document root
    # concurs with nginx's one
    #
    #location ~ /\.ht {
    #       deny all;
    #}
    }


    # Virtual Host configuration for example.com
    #
    # You can move that to a different file under sites-available/ and symlink that
    # to sites-enabled/ to enable it.
    #
    #server {
    #       listen 80;
    #       listen [::]:80;
    #
    #       server_name example.com;
    #
    #       root /var/www/example.com;
    #       index index.html;
    #
    #       location / {
    #               try_files $uri $uri/ =404;
    #       }
    #}
    #
    server {
    #the port your site will be served on
            listen      443     ssl;
    # the domain name it will serve for
            server_name example.com; # substitute your machine's IP address or FQDN
                    access_log  /var/log/nginx/example.com_access.log combined;
            error_log   /var/log/nginx/example.com_error.log error;
            charset     utf-8;

            ssl_certificate     /your/path/project/conf.d/django.crt;
            ssl_certificate_key /your/path/project/conf.d/django.key;

            error_page 497 https://$server_name$request_uri;

    # max upload size
            client_max_body_size 75M;   # adjust to taste

    # Django media
                    location /media  {
                            alias /home/ubuntu/2021contest/Stroke_Self_Diagnosis/media;  # your Django project's media files - amend as required
                    }

            location /static {
                    alias /home/ubuntu/2021contest/Stroke_Self_Diagnosis/static; # your Django project's static files - amend as required
            }

    # Finally, send all non-media requests to the Django server.
            location / {
                    proxy_pass      http://localhost:8000/;
                    proxy_redirect  off;

                    proxy_set_header        Host            $http_host;
                    proxy_set_header        X-Real-IP       $remote_addr;
                    proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;

                    uwsgi_pass      django;
                    include         /etc/nginx/uwsgi_params; # the uwsgi_params file you installed
            }
    }
    
    -->
