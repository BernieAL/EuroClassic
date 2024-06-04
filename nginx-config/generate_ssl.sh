#!/bin/bash

# Remove previous versions of SSL files
rm -f rootCA.key rootCA.crt server.key server.crt server.csr fullchain.pem ssl-params.conf


# Create a Certificate Authority (CA)
openssl genrsa -out rootCA.key 2048
openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 1024 -out rootCA.crt

# Generate a Certificate Signing Request (CSR) for the server
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr

# Sign the CSR with the CA to generate the server certificate
openssl x509 -req -in server.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -out server.crt -days 500 -sha256

# Create the full chain certificate
cat server.crt rootCA.crt > fullchain.pem

# Create ssl-params.conf
cat <<EOF > ssl-params.conf
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
ssl_ciphers "EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH";
ssl_ecdh_curve secp384r1;
ssl_session_cache shared:SSL:10m;
ssl_session_tickets off;
ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
EOF

echo "SSL certificates and related files generated successfully."
